# -*- coding: utf-8 -*-

from edx_rbac.admin.forms import UserRoleAssignmentAdminForm

from ecommerce.core.models import EcommerceFeatureRoleAssignment


class EcommerceFeatureRoleAssignmentAdminForm(UserRoleAssignmentAdminForm):
    """
    Admin form for EcommerceFeatureRoleAssignmentAdmin
    """

    class Meta(object):
        """
        Meta class for EcommerceFeatureRoleAssignmentAdminForm.
        """

        model = EcommerceFeatureRoleAssignment
        fields = ('user', 'role')
