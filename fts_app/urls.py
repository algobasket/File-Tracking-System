from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views 


urlpatterns = [ 
    # Authentication
    path('', views.auth_views.login, name='login'),
    path('login/', views.auth_views.login, name='login'),
    path('logout/', views.auth_views.logout, name='logout'),
    path('install/', views.install_views.install, name='install'),

    # Dashboard
    path('dashboard/dakghar/', views.dashboard_views.dakghar, name='dashboard-dakghar'),
    path('dashboard/dakghar/documents', views.dashboard_views.dakghar_documents, name='dashboard-dakghar-documents'),
    path('dashboard/dakghar/documents-forward/<int:doc_id>/', views.dashboard_views.dakghar_documents_forward, name='dakghar-documents-forward'),
    path('dashboard/dakghar/document-delete/<int:doc_id>/', views.dashboard_views.dakghar_delete_document, name='dakghar-delete-documents'),     
    path('dashboard/gms/', views.dashboard_views.manager, name='dashboard-gms'), 
    path('dashboard/manager/', views.dashboard_views.manager, name='dashboard-manager'),

    # Download link
    path('operation/download/<int:file_name>/', views.dashboard_views.download_document, name='download-document'),


    # Department 
    path('dashboard/department/', views.dashboard_views.dashboard_department, name='dashboard-department'),
    path('dashboard/account/', views.dashboard_views.dashboard_account, name='dashboard-account'), 
    path('dashboard/department/outgoing-correspondence', views.dashboard_views.outgoing_correspondence_department, name='dashboard-department-outgoing-correspondence'),
    path('dashboard/department/incoming-correspondence', views.dashboard_views.incoming_correspondence_department, name='dashboard-department-incoming-correspondence'),

    # Operations
    path('operation/list-correspondence/', views.correspondences_views.list_correspondence, name='list-correspondence'), 
    path('operation/add-correspondence/', views.correspondences_views.add_correspondence, name='add-correspondence'),
    path('operation/edit-correspondence/<int:correspondence_id>/', views.correspondences_views.edit_correspondence, name='edit-correspondence'),
    path('operation/monitoring-documents/', views.correspondences_views.monitoring_documents, name='monitoring-documents'),
    path('operation/monitoring-documents/delete/<int:doc_id>/', views.correspondences_views.delete_monitoring_document, name='delete-monitoring-document'),
    path('operation/monitoring-documents/view/<int:doc_id>/<int:msg_id>', views.correspondences_views.view_monitoring_document, name='view-monitoring-document'),
    path('operation/monitoring-correspondence-documents/view/<int:doc_id>/<int:correspondence_map_id>', views.correspondences_views.view_correspondence_document, name='view-correspondence-document'),
    path('operation/forward-departmental-correspondence/<int:correspondence_map_id>/<int:correspondence_id>/', views.correspondences_views.forward_departmental_correspondence, name='forward-departmental-correspondence'),
    path('operation/forward-correspondence/<int:correspondence_id>', views.correspondences_views.forward_correspondence, name='forward-correspondence'),
    path('operation/delete-correspondence/<int:correspondence_id>/', views.correspondences_views.delete_correspondence, name='delete-correspondence'), 



    # Site
    path('documents/daily-entry-report', views.site_views.daily_entry_report, name='daily-entry-report'), 
    path('documents/red-cornered-open/', views.site_views.red_cornered_open, name='red-cornered-open'),
    path('documents/red-cornered-closed/', views.site_views.red_cornered_closed, name='red-cornered-closed'),
    path('documents/all-documents/open-closed', views.site_views.all_documents_open_closed, name='all-documents-open-closed'),
    path('documents/all-documents/closed', views.site_views.all_documents_closed, name='all-documents-closed'),



    # Ajax Calls 
    path('ajax/ajaxGetSubDepartment/', views.ajax_views.ajaxGetSubDepartment, name='ajaxGetSubDepartment'),
    path('ajax/ajaxGetRoleUsers/', views.ajax_views.ajaxGetRoleUsers, name='ajaxGetRoleUsers'),   
    path('ajax/ajaxGetDepartmentRoles/', views.ajax_views.ajaxGetDepartmentRoles, name='ajaxGetDepartmentRoles'), 
    path('ajax/ajaxCorrespondenceMapIsStatus/', views.ajax_views.ajaxCorrespondenceMapIsStatus, name='ajaxCorrespondenceMapIsStatus'), 
    path('ajax/ajaxChangeUserPassword/', views.ajax_views.ajaxChangeUserPassword, name='ajaxChangeUserPassword'), 


    # Test 
    # path('test/addAdmin/', views.test_views.add_admin, name='addAdmin'), 

    # Admin
    path('dashboard/admin/', views.admin.admin_views.dashboard, name='dashboard-admin'),
    path('backend-admin/list-users/', views.admin.operations_views.list_users, name='admin-list-users'),
    path('backend-admin/add-user/', views.admin.operations_views.add_user, name='admin-add-user'),
    path('backend-admin/edit-user/<int:user_id>/', views.admin.operations_views.edit_user, name='admin-edit-user'),
    path('backend-admin/delete-user/<int:user_id>/', views.admin.operations_views.delete_user, name='admin-delete-user'),
    path('backend-admin/add-role/', views.admin.operations_views.add_role, name='admin-add-role'), 
    path('backend-admin/delete-role/<int:role_id>/', views.admin.operations_views.delete_role, name='admin-delete-role'),  
    path('backend-admin/list-roles/', views.admin.operations_views.list_roles, name='admin-list-roles'),

    path('backend-admin/list-correspondence/', views.admin.operations_views.list_correspondence, name='admin-list-correspondence'),  
    path('backend-admin/add-correspondence/', views.admin.operations_views.add_correspondence, name='admin-add-correspondence'),
    path('backend-admin/edit-correspondence/<int:correspondence_id>/', views.admin.operations_views.edit_correspondence, name='admin-edit-correspondence'),
    path('backend-admin/delete-correspondence/<int:correspondence_id>/', views.admin.operations_views.delete_correspondence, name='admin-delete-correspondence'),
    path('backend-admin/forward-correspondence/<int:correspondence_id>/', views.admin.operations_views.forward_correspondence, name='admin-forward-correspondence'), 
    path('backend-admin/forward-correspondence/list/', views.admin.operations_views.forward_correspondence_list, name='admin-forward-correspondence-list'), 
    path('backend-admin/monitoring-documents/', views.admin.operations_views.monitoring_documents, name='admin-monitoring-documents'), 
    path('backend-admin/monitoring-documents/delete/<int:doc_id>/', views.admin.operations_views.delete_monitoring_document, name='admin-delete-monitoring-document'),    
    path('backend-admin/monitoring-documents/view/<int:doc_id>/<int:msg_id>', views.admin.operations_views.view_monitoring_document, name='admin-view-monitoring-document'),    

    path('backend-admin/department/', views.admin.department_views.list_department, name='admin-list-department'),     
    path('backend-admin/department/create', views.admin.department_views.create_department, name='admin-create-department'), 
    path('backend-admin/department/edit/<int:department_id>/', views.admin.department_views.update_department, name='admin-update-department'),  
    path('backend-admin/department/delete/<int:department_id>/', views.admin.department_views.delete_department, name='admin-delete-department'),    
    path('backend-admin/sub-department/', views.admin.department_views.list_sub_department, name='admin-list-sub-department'),  
    path('backend-admin/sub-department/create', views.admin.department_views.create_sub_department, name='admin-create-sub-department'),  
    path('backend-admin/sub-department/edit/<int:sub_department_id>/', views.admin.department_views.update_sub_department, name='admin-update-sub-department'), 
    path('backend-admin/sub-department/delete/<int:sub_department_id>/', views.admin.department_views.delete_sub_department, name='admin-delete-sub-department') 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
