function StaffManage() {

}


StaffManage.prototype.ListenDelPermissionEvent = function () {
    var delBtn = $('.delete-btn');
    delBtn.click(function () {
        var currentBtn = $(this);
        var telephone = currentBtn.attr('data-permission-telephone');
        blogalert.alertConfirm({
            'title': '确认删除权限吗？',
            'confirmCallback': function () {
                // console.log('123');
                blogajax.post({
                    'url': '/cms/del_permission/',
                    'data': {
                        'telephone': telephone,
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.messageBox.showSuccess('删除成功！');
                            window.location = window.location.href;
                        } else {
                            window.messageBox.showError(result['message']);
                        }
                    }
                });
            }
        });
    });
};


StaffManage.prototype.ListenDelStaffEvent = function () {
    var delBtn = $('.del-user-btn');
    delBtn.click(function () {
        var currentBtn = $(this);
        var telephone = currentBtn.attr('data-staff-telephone');
        blogalert.alertConfirm({
            'title': '确认删除员工吗？',
            'confirmCallback': function () {
                blogajax.post({
                    'url': '/cms/del_staff/',
                    'data': {
                        'telephone': telephone,
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.messageBox.showSuccess('删除成功！');
                            window.location = window.location.href;
                        } else {
                            window.messageBox.showError(result['message']);
                        }
                    }
                });
            }
        });
    });
};

StaffManage.prototype.listenAddManageEvent = function () {
    var addBtn = $("#add-group-btn");
    addBtn.click(function () {
        event.preventDefault();
        var telephone = $("input[name='telephone']").val();
        var group = $("select[name='group']").val();
        blogalert.alertConfirm({
            'title': '确认添加吗？',
            'confirmCallback': function () {
                // console.log('123');
                blogajax.post({
                    'url': '/cms/staff_manage/',
                    'data': {
                        'telephone': telephone,
                        'group': group,
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.messageBox.showSuccess('添加成功！');
                            window.location = window.location.href;
                        } else {
                            blogalert.close();
                            window.messageBox.showError(result['message']);
                        }
                    }
                });
            }
        });
    })
};

StaffManage.prototype.run = function () {
    this.ListenDelPermissionEvent();
    this.listenAddManageEvent();
    this.ListenDelStaffEvent();
};


$(function () {
    var staffmanage = new StaffManage();
    staffmanage.run();
});