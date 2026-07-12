from django.test import TestCase
from django.urls import reverse

from core.models import Branch, PYQ


class PYQListAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cse = Branch.objects.create(code='CSE', name='Computer Science')
        electrical = Branch.objects.create(code='EE', name='Electrical')

        cls.data_structures = PYQ.objects.create(
            subject='Data Structures',
            branch=cse,
            semester=3,
            year=2024,
            exam_type='F',
            pdf_link='https://example.com/data-structures.pdf',
        )
        PYQ.objects.create(
            subject='Operating Systems',
            branch=cse,
            semester=4,
            year=2023,
            exam_type='mid',
            pdf_link='https://example.com/operating-systems.pdf',
        )
        PYQ.objects.create(
            subject='Basic Electrical Engineering',
            branch=electrical,
            semester=2,
            year=2022,
            exam_type='end',
            pdf_link='https://example.com/electrical.pdf',
        )

    def test_searches_subject_and_returns_pdf_url(self):
        response = self.client.get(reverse('api:pyqs_list'), {'search': 'data structures'})

        self.assertEqual(response.status_code, 200)
        papers = response.json()['pyqs']
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]['id'], self.data_structures.id)
        self.assertEqual(papers[0]['pdf_url'], 'https://example.com/data-structures.pdf')

    def test_searches_branch_code_or_name_case_insensitively(self):
        by_code = self.client.get(reverse('api:pyqs_list'), {'search': 'ee'})
        by_name = self.client.get(reverse('api:pyqs_list'), {'q': 'ELECTRICAL'})

        self.assertEqual(len(by_code.json()['pyqs']), 1)
        self.assertEqual(len(by_name.json()['pyqs']), 1)
        self.assertEqual(by_name.json()['pyqs'][0]['branch'], 'EE')

    def test_searches_numeric_year(self):
        response = self.client.get(reverse('api:pyqs_list'), {'search': '2023'})

        papers = response.json()['pyqs']
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]['subject'], 'Operating Systems')

    def test_combines_search_with_year_and_exam_type_filters(self):
        response = self.client.get(
            reverse('api:pyqs_list'),
            {'search': 'computer', 'year': '2024', 'exam_type': 'F'},
        )

        papers = response.json()['pyqs']
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]['id'], self.data_structures.id)

    def test_pyq_page_renders_search_and_api_endpoint(self):
        response = self.client.get(reverse('pyq'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="search-pyq"')
        self.assertContains(response, reverse('api:pyqs_list'))
