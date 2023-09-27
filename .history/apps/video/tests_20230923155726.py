from django.test import TestCasfrom django.core.files.uploadedfile import SimpleUploadedFile
from .models import  *

class ModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='TestCategory')
        video_image = SimpleUploadedFile("video.jpg", b"file_content")
        self.video = Video.objects.create(
            category=self.category,
            title='TestVideo',
            videos=video_image,
            description='Test description',
        )
        
        image = SimpleUploadedFile("preview.jpg", b"file_content")
        self.video_preview = VideoPreview.objects.create(
            image=image,
            product=self.video,
        )

    def test_category_creation(self):
        category = Category.objects.get(title='TestCategory')
        self.assertEqual(category.title, 'TestCategory')
        self.assertEqual(category.slug, 'testcategory')

    def test_video_creation(self):
        video = Video.objects.get(title='TestVideo')
        self.assertEqual(video.title, 'TestVideo')
        self.assertEqual(video.slug, 'testvideo')
        self.assertEqual(video.category, self.category)
        self.assertEqual(video.in_stock, False)

    def test_video_preview_creation(self):
        video_preview = VideoPreview.objects.get(product=self.video)
        self.assertIsNotNone(video_preview.image)
        self.assertEqual(video_preview.product, self.video)

    def test_str_methods(self):
        category = Category.objects.get(title='TestCategory')
        video = Video.objects.get(title='TestVideo')
        video_preview = VideoPreview.objects.get(product=self.video)

        self.assertEqual(str(category), 'TestCategory')
        self.assertEqual(str(video), 'TestVideo')
        self.assertEqual(str(video_preview), f'VideoPreview object ({video_preview.id})')

    def test_video_description(self):
        video = Video.objects.get(title='TestVideo')
        self.assertEqual(video.get_description(), 'Test description')
