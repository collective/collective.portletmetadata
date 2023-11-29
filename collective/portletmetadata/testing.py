from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer

import collective.portletmetadata


FIXTURE = PloneWithPackageLayer(
    zcml_package=collective.portletmetadata,
    zcml_filename="configure.zcml",
    gs_profile_id="collective.portletmetadata:default",
    name="CollectivePortletMetadataFixture",
)
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="CollectivePortletMetadata:IntegrationTesting",
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name="CollectivePortletMetadata:FunctionalTesting",
)
