import os

from django.conf import settings
from sorl.thumbnail.engines.base import EngineBase as ThumbnailEngineBase
from sorl_watermarker.parsers import parse_geometry
from sorl_watermarker.utils import setting

STATIC_ROOT = getattr(settings, 'MEDIA_ROOT')


class WatermarkEngineBase(ThumbnailEngineBase):
    """
    Extend sorl.thumbnail base engine to support watermarks.
    """
    def create(self, image, geometry, options):
        image = super(WatermarkEngineBase, self).create(image, geometry,
                                                        options)
        if (setting('THUMBNAIL_WATERMARK_ALWAYS', True) or
                'watermark'       in options or
                'watermark_pos'   in options or
                'watermark_size'  in options or
                'watermark_alpha' in options):
            image = self.watermark(image, options)
        return image

    def watermark(self, image, options):
        """
        Wrapper for ``_watermark``

        Takes care of all the options handling.
        """
        if not setting('THUMBNAIL_WATERMARK', False):
            raise AttributeError('Trying to apply a watermark, '
                                 'however no THUMBNAIL_WATERMARK defined')

        watermark_path = os.path.join(STATIC_ROOT, setting('THUMBNAIL_WATERMARK'))
        if not 'watermark_alpha' in options:
            options['watermark_alpha'] = setting('THUMBNAIL_WATERMARK_OPACITY', 1)

        if not 'watermark_size' in options and setting('THUMBNAIL_WATERMARK_SIZE'):
            options['watermark_size'] = setting('THUMBNAIL_WATERMARK_SIZE')
        elif 'watermark_size' in options:
            options['watermark_size'] = parse_geometry(
                                            options['watermark_size'],
                                            self.get_image_ratio(image),
                                        )
        else:
            options['watermark_size'] = False

        return self._watermark(image, watermark_path,
                               options['watermark_alpha'],
                               options['watermark_size'])
