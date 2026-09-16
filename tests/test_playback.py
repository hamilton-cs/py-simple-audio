"""
Tests playing audio.

These tests exercise the native per-platform backend end to end: buffer
allocation, the OS-specific playback API (CoreAudio / WinMM / ALSA), the
buffer-draining callback thread, and cleanup.

These tests were written as regression tests for
the PyMem_Malloc/PyMem_Free -> PyMem_RawMalloc/PyMem_RawFree fix
and the play_os()/fill_buffer() empty-buffer double-free bug.

Note: If the CI image does not have a usable audio output device,
the tests are skipped.
"""

import math
import time
import unittest

import simpleaudiohamiltoncs as sa
from simpleaudiohamiltoncs._simpleaudiohamiltoncs import simpleaudiohamiltoncsError


def _generate_tone(duration_s, sample_rate=44100, freq=440,
                    num_channels=1, bytes_per_channel=2):
    """Build a short, valid PCM sine tone as raw bytes for play_buffer().

    8-bit samples are unsigned (WAV convention); 16/24-bit are signed.
    """
    num_samples = int(duration_s * sample_rate)
    signed = bytes_per_channel != 1
    amplitude = 2 ** (bytes_per_channel * 8 - 1) - 1
    frames = bytearray()
    for i in range(num_samples):
        value = int(amplitude * 0.2 * math.sin(2 * math.pi * freq * i / sample_rate))
        sample = value if signed else value + 128
        packed = sample.to_bytes(bytes_per_channel, byteorder="little", signed=signed)
        frames += packed * num_channels
    return bytes(frames)


def _skip_if_no_device(test_method):
    """Turn "no audio device on this machine/CI image" into a skip instead
    of a failure"""
    def wrapper(self, *args, **kwargs):
        try:
            return test_method(self, *args, **kwargs)
        except simpleaudiohamiltoncsError as exc:
            raise unittest.SkipTest("no audio output device available: %s" % exc)
    return wrapper


class TestRealPlayback(unittest.TestCase):

    # Shorter than one internal playback buffer (~50ms at the current
    # 100ms/NUM_BUFS latency setting) -- exercises the "audio finishes
    # inside the very first buffer" path.
    SHORT_TONE = _generate_tone(0.05)
    # Long enough to span several internal buffers and hand-offs between
    # the main thread and the native buffer-draining thread.
    LONG_TONE = _generate_tone(1.0)

    @_skip_if_no_device
    def test_play_and_wait_done(self):
        playback = sa.play_buffer(self.SHORT_TONE, 1, 2, 44100)
        playback.wait_done()
        self.assertFalse(playback.is_playing())

    @_skip_if_no_device
    def test_repeated_playback_stress(self):
        """
        Regression test for the PyMem_Malloc/PyMem_Free race:
        buffers were allocated on the main thread (which holds the GIL)
        but freed on the native buffer-draining thread (which never
        acquires it), corrupting CPython's allocator under timing-
        dependent conditions. A single play() call was not a reliable
        repro; repeating play+wait many times back-to-back gives the
        race many chances to happen. A crash here kills the whole test
        process instead of reporting a normal failure -- that is
        the signal to watch for on CI.
        """
        for _ in range(50):
            playback = sa.play_buffer(self.SHORT_TONE, 1, 2, 44100)
            playback.wait_done()

    @_skip_if_no_device
    def test_stop_short_circuits_playback(self):
        playback = sa.play_buffer(self.LONG_TONE, 1, 2, 44100)
        time.sleep(0.05)
        playback.stop()
        playback.wait_done()
        self.assertFalse(playback.is_playing())

    @_skip_if_no_device
    def test_concurrent_playback_and_stop_all(self):
        """Stresses the play_list_item linked list / mutex handling
        (new_list_item/delete_list_item) with several simultaneous
        playbacks instead of one at a time."""
        playbacks = [sa.play_buffer(self.LONG_TONE, 1, 2, 44100) for _ in range(5)]
        time.sleep(0.05)
        sa.stop_all()
        for playback in playbacks:
            playback.wait_done()
            self.assertFalse(playback.is_playing())

    @_skip_if_no_device
    def test_stereo_and_alternate_sample_rate(self):
        """Covers a second, less-common parameter combination (stereo,
        16000 Hz) so coverage isn't limited to one exact code path."""
        tone = _generate_tone(0.1, sample_rate=16000, num_channels=2)
        playback = sa.play_buffer(tone, 2, 2, 16000)
        playback.wait_done()
        self.assertFalse(playback.is_playing())

    @_skip_if_no_device
    def test_8bit_playback(self):
        """8-bit is unsigned, unlike every other test here."""
        tone = _generate_tone(0.1, bytes_per_channel=1)
        playback = sa.play_buffer(tone, 1, 1, 44100)
        playback.wait_done()
        self.assertFalse(playback.is_playing())

    @_skip_if_no_device
    def test_24bit_playback(self):
        """24-bit (packed 3-byte samples) is untested elsewhere."""
        tone = _generate_tone(0.1, bytes_per_channel=3)
        playback = sa.play_buffer(tone, 1, 3, 44100)
        playback.wait_done()
        self.assertFalse(playback.is_playing())


class TestEmptyBufferEdgeCase(unittest.TestCase):
    """
    Regression test for the double-free / use-after-free bug that used to
    exist in play_os()'s initial buffer-priming loop
    """

    def test_empty_buffer_does_not_crash(self):
        # A zero-length buffer passes _play_buffer()'s own validations
        # triggering the bug.
        playback = sa.play_buffer(b"", 1, 2, 44100)
        playback.wait_done()
        self.assertFalse(playback.is_playing())


if __name__ == "__main__":
    unittest.main()
