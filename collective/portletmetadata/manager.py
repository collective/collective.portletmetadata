from zope.interface import Interface
from zope.component import adapter
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from Acquisition import aq_inner, aq_parent

from Products.CMFPlone.defaultpage import check_default_page_via_view
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.interfaces import IColumn
from plone.app.portlets.manager import ColumnPortletManagerRenderer as \
    BaseColumnPortletManagerRenderer


@adapter(Interface, IDefaultBrowserLayer, IBrowserView, IColumn)
class ColumnPortletManagerRenderer(BaseColumnPortletManagerRenderer):

    template = ViewPageTemplateFile('column.pt')

    def available(self, info):
        """Only make available on definition context
        """
        if info['settings'].get('is_local', False):
            compare_context = self.context
            if check_default_page_via_view(self.context, self.request):
                compare_context = aq_parent(aq_inner(self.context))
            if '/'.join(compare_context.getPhysicalPath()) != info['key']:
                return False

        return True
