from aiortc.codecs import PCMA_CODEC, PCMU_CODEC, get_decoder, get_encoder
from aiortc.codecs.g711 import (PcmaDecoder, PcmaEncoder, PcmuDecoder,
                                PcmuEncoder)
from aiortc.jitterbuffer import JitterFrame
from aiortc.mediastreams import AudioFrame

from .codecs import CodecTestCase


class PcmaTest(CodecTestCase):
    def test_decoder(self):
        decoder = get_decoder(PCMA_CODEC)
        self.assertTrue(isinstance(decoder, PcmaDecoder))

        frames = decoder.decode(JitterFrame(data=b'\xd5' * 160, timestamp=0))
        self.assertEqual(len(frames), 1)
        frame = frames[0]
        self.assertEqual(frame.channels, 1)
        self.assertEqual(frame.data, b'\x08\x00' * 160)
        self.assertEqual(frame.sample_rate, 8000)
        self.assertEqual(frame.timestamp, 0)

    def test_encoder_mono_8hz(self):
        encoder = get_encoder(PCMA_CODEC)
        self.assertTrue(isinstance(encoder, PcmaEncoder))

        frame = AudioFrame(
            channels=1,
            data=b'\x00\x00' * 160,
            sample_rate=8000,
            timestamp=0)
        data = encoder.encode(frame)
        self.assertEqual(data, b'\xd5' * 160)

    def test_encoder_stereo_8khz(self):
        encoder = get_encoder(PCMA_CODEC)
        self.assertTrue(isinstance(encoder, PcmaEncoder))

        frame = AudioFrame(
            channels=2,
            data=b'\x00\x00' * 2 * 160,
            sample_rate=8000,
            timestamp=0)
        data = encoder.encode(frame)
        self.assertEqual(data, b'\xd5' * 160)

    def test_encoder_stereo_48khz(self):
        encoder = get_encoder(PCMA_CODEC)
        self.assertTrue(isinstance(encoder, PcmaEncoder))

        frame = AudioFrame(
            channels=2,
            data=b'\x00\x00' * 2 * 960,
            sample_rate=48000,
            timestamp=0)
        data = encoder.encode(frame)
        self.assertEqual(data, b'\xd5' * 160)

    def test_roundtrip(self):
        self.roundtrip_audio(PCMA_CODEC, output_channels=1, output_sample_rate=8000)


class PcmuTest(CodecTestCase):
    def test_decoder(self):
        decoder = get_decoder(PCMU_CODEC)
        self.assertTrue(isinstance(decoder, PcmuDecoder))

        frames = decoder.decode(JitterFrame(data=b'\xff' * 160, timestamp=0))
        self.assertEqual(len(frames), 1)
        frame = frames[0]
        self.assertEqual(frame.channels, 1)
        self.assertEqual(frame.data, b'\x00\x00' * 160)
        self.assertEqual(frame.sample_rate, 8000)
        self.assertEqual(frame.timestamp, 0)

    def test_encoder_mono_8hz(self):
        encoder = get_encoder(PCMU_CODEC)
        self.assertTrue(isinstance(encoder, PcmuEncoder))

        frame = AudioFrame(
            channels=1,
            data=b'\x00\x00' * 160,
            sample_rate=8000,
            timestamp=0)
        data = encoder.encode(frame)
        self.assertEqual(data, b'\xff' * 160)

    def test_encoder_stereo_8khz(self):
        encoder = get_encoder(PCMU_CODEC)
        self.assertTrue(isinstance(encoder, PcmuEncoder))

        frame = AudioFrame(
            channels=2,
            data=b'\x00\x00' * 2 * 160,
            sample_rate=8000,
            timestamp=0)
        data = encoder.encode(frame)
        self.assertEqual(data, b'\xff' * 160)

    def test_encoder_stereo_48khz(self):
        encoder = get_encoder(PCMU_CODEC)
        self.assertTrue(isinstance(encoder, PcmuEncoder))

        frame = AudioFrame(
            channels=2,
            data=b'\x00\x00' * 2 * 960,
            sample_rate=48000,
            timestamp=0)
        data = encoder.encode(frame)
        self.assertEqual(data, b'\xff' * 160)

    def test_roundtrip(self):
        self.roundtrip_audio(PCMU_CODEC, output_channels=1, output_sample_rate=8000)
