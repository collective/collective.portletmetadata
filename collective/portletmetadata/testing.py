from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import zope
from Products.CMFCore.utils import getToolByName
from zope.configuration import xmlconfig
from plone.testing.zope import Browser
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
import doctest
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from zope.component import getUtility
from plone.portlets.interfaces import IPortletManager
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletAssignmentMapping
from collective.portletmetadata.interfaces import IPortletMetadata



class PortletMetadata(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.monkeypatcher
        xmlconfig.file("configure.zcml", collective.monkeypatcher, context=configurationContext)
        import Products.CMFCore
        xmlconfig.file("configure.zcml", Products.CMFCore, context=configurationContext)
        import plone.app.portlets
        xmlconfig.file("configure.zcml", plone.app.portlets, context=configurationContext)
        import z3c.jbot
        xmlconfig.file("meta.zcml", z3c.jbot, context=configurationContext)
        import z3c.unconfigure
        xmlconfig.file("meta.zcml", z3c.unconfigure, context=configurationContext)

        import collective.portletmetadata
        xmlconfig.file(
            "configure.zcml", collective.portletmetadata, context=configurationContext
        )

        zope.installProduct(app, "plone.app.portlets")
        # zope.installProduct(app, "collective.portletmetadata")
        #self.app = app

        # Include testing profile with test search portlet
        xmlconfig.file(
            "configure.zcml", collective.portletmetadata.tests, context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, "plone.app.contenttypes:default")
        applyProfile(portal, "collective.portletmetadata:default")
        applyProfile(portal, "collective.portletmetadata:testing")

        setRoles(portal, TEST_USER_ID, ["Manager"])
        login(portal, TEST_USER_NAME)

        # Prepare test content
        pw = getToolByName(portal, "portal_workflow")
        pw.setDefaultChain("simple_publication_workflow")
        portal.invokeFactory("Folder", id="folder", title="Test Folder")
        portal.invokeFactory("Folder", id="news", title="News")
        portal.invokeFactory("Folder", id="users", title="Users")
        portal.invokeFactory("Folder", id="events", title="Events")
        pw.doActionFor(portal.news, "publish")

        manager = getUtility(IPortletManager, name="plone.leftcolumn")
        assignments = getMultiAdapter(
            (portal, manager), IPortletAssignmentMapping
        )
        assignment = assignments['test.portlet1']
        # settings = IPortletAssignmentSettings(assignment)
        metadata = IPortletMetadata(assignment)
        metadata.css_class = "myclass"



PLONE_APP_PORTLETS_FIXTURE = PortletMetadata()
PLONE_APP_PORTLETS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_APP_PORTLETS_FIXTURE,),
    name="PortletMetadata:Integration",
)
PLONE_APP_PORTLETS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_APP_PORTLETS_FIXTURE,),
    name="PortletMetadata:Functional",
)

OPTIONFLAGS = (
    doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
)