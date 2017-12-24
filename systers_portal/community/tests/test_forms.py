from django.contrib.auth.models import User, Group
from django.test import TestCase


from community.forms import (EditCommunityForm, AddCommunityPageForm,
                             EditCommunityPageForm, PermissionGroupsForm,
                             RequestCommunityForm, AddCommunityForm)
from community.models import Community, CommunityPage, RequestCommunity
from users.models import SystersUser


class RequestCommunityFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)

    def test_request_community_form(self):
        invalid_data = {'name': 'Bar',
                        'slug': 'foo'}
        form = RequestCommunityForm(data=invalid_data, user=self.user)
        self.assertFalse(form.is_valid())

        data = {'name': 'Bar',
                'slug': 'foo',
                'order': '1'}
        form = RequestCommunityForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.community_request = RequestCommunity.objects.get()
        self.assertEqual(self.community_request.name, 'Bar')
        self.assertEqual(self.community_request.slug, 'foo')
        self.assertEqual(self.community_request.user, self.systers_user)


class EditCommunityRequestFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.community_request = RequestCommunity.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  user=self.systers_user)
    def test_edit_community_form(self):
        data = {'name': 'Bar',
                'slug': 'bar',
                'order': 1,
                'user': self.user}
        form = CommunityForm(data=data, instance=self.community_request)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.community_request.name, 'Bar')
        self.assertEqual(self.community_request.slug, 'bar')


class EditCommunityFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  admin=self.systers_user)

    def test_edit_community_form(self):
        """Test community form"""
        data = {'name': 'Bar',
                'slug': 'bar',
                'order': 1,
                'admin': self.systers_user}
        form = EditCommunityForm(data=data, instance=self.community)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.community.name, 'Bar')
        self.assertEqual(self.community.slug, 'bar')


class AddCommunityFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)

    def test_add_community_form(self):
        """Test add Community Form"""
        invalid_data = {'name': 'Bar',
                        'slug': 'foo'}
        form = AddCommunityForm(data=invalid_data, admin=self.systers_user)
        self.assertFalse(form.is_valid())

        data = {'name': 'Bar',
                'slug': 'foo',
                'order': '1'}
        form = AddCommunityForm(data=data, admin=self.systers_user)
        self.assertTrue(form.is_valid())
        form.save()
        self.community = Community.objects.get()
        self.assertEqual(self.community.name, 'Bar')
        self.assertEqual(self.community.slug, 'foo')
        self.assertEqual(self.community.admin, self.systers_user)


class AddCommunityPageFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  admin=self.systers_user)

    def test_add_community_page_form(self):
        """Test add CommunityPage form"""
        invalid_data = {'title': "something"}
        form = AddCommunityPageForm(data=invalid_data, author=self.user,
                                    community=self.community)
        self.assertFalse(form.is_valid())

        data = {'slug': 'foo',
                'title': 'Foo',
                'order': 1,
                'content': "Rainbows and ponies"}
        form = AddCommunityPageForm(data=data, author=self.user,
                                    community=self.community)
        self.assertTrue(form.is_valid())
        form.save()
        resource = CommunityPage.objects.get()
        self.assertEqual(resource.title, 'Foo')
        self.assertEqual(resource.author, self.systers_user)


class EditCommunityPageFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  admin=self.systers_user)

    def test_edit_community_page_form(self):
        """Test edit community page"""
        incomplete_data = {'slug': 'slug'}
        form = EditCommunityPageForm(data=incomplete_data)
        self.assertFalse(form.is_valid())

        page = CommunityPage.objects.create(slug="foo", title="Foo page",
                                            order=1,
                                            author=self.systers_user,
                                            content="Content",
                                            community=self.community)
        data = {'slug': 'bar',
                'title': 'Bar page',
                'order': 2,
                'content': "New content"}
        form = EditCommunityPageForm(instance=page, data=data)
        self.assertTrue(form.is_valid())
        form.save()
        page = CommunityPage.objects.get()
        self.assertEqual(page.slug, 'bar')
        self.assertEqual(page.order, 2)
        self.assertEqual(page.title, "Bar page")


class PermissionGroupsFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  admin=self.systers_user)

    def test_permissions_groups_form(self):
        """Test permission groups form"""
        invalid_form = PermissionGroupsForm(user=self.systers_user,
                                            community=self.community)
        self.assertFalse(invalid_form.is_valid())

        form = PermissionGroupsForm(user=self.systers_user, data={},
                                    community=self.community)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.initial, {})
        groups = [Group.objects.get(name="Foo: Content Manager"),
                  Group.objects.get(name="Foo: Content Contributor"),
                  Group.objects.get(name="Foo: User and Content Manager")]
        self.assertCountEqual(form.groups, groups)
        form.save()
        for group in groups:
            self.assertFalse(self.systers_user.is_group_member(group))

        self.systers_user.join_group(groups[0])
        form = PermissionGroupsForm(user=self.systers_user, data={},
                                    community=self.community,
                                    initial={'groups': [groups[0].pk]})
        self.assertTrue(form.is_valid())
        self.assertCountEqual(form.initial['groups'], [groups[0].pk])
        form.save()

        form = PermissionGroupsForm(user=self.systers_user,
                                    community=self.community,
                                    data={'groups': [group.pk for group
                                                     in groups]})
        self.assertTrue(form.is_valid())
        form.save()
        for group in groups:
            self.assertTrue(self.systers_user.is_group_member(group))

        form = PermissionGroupsForm(user=self.systers_user,
                                    community=self.community,
                                    data={'groups': [groups[0].pk]})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(self.systers_user.is_group_member(groups[0]))
        self.assertFalse(self.systers_user.is_group_member(groups[1]))
        self.assertFalse(self.systers_user.is_group_member(groups[2]))
