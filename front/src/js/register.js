function Login() {
    let self = this;
    self.registerWrapper = $('#register-box');
    self.loginWrapper = $('#login-box');
    self.editWrapper = $('#edit-box');
}

Login.prototype.registerShowEvent = function () {
    let self = this;
    self.registerWrapper.show();
};

Login.prototype.registerHideEvent = function () {
    let self = this;
    self.registerWrapper.hide();
};

Login.prototype.loginShowEvent = function () {
    let self = this;
    self.loginWrapper.show();
};

Login.prototype.loginHideEvent = function () {
    let self = this;
    self.loginWrapper.hide();
};

Login.prototype.editShowEvent = function () {
    let self = this;
    self.editWrapper.show();
};

Login.prototype.editHideEvent = function () {
    let self = this;
    self.editWrapper.hide();
};


Login.prototype.listenBtnEvent = function () {

    let self = this;
    let registerBtn = $('#register-btn');
    let registerCloseBtn = $('.register-close-btn');
    let loginBtn = $('#login-btn');
    let loginCloseBtn = $('.login-close-btn');
    let editBtn = $('#edit-btn');
    let editCloseBtn = $('.edit-close-btn');

    registerBtn.click(function () {
        self.registerShowEvent();
    });
    registerCloseBtn.click(function () {
        self.registerHideEvent();
    });

    loginBtn.click(function () {
        self.loginShowEvent();
    });
    loginCloseBtn.click(function () {
        self.loginHideEvent()
    });

    editBtn.click(function () {
        self.editShowEvent();
    });

    editCloseBtn.click(function () {
        self.editHideEvent();
    });
};


Login.prototype.run = function () {
    let self = this;
    self.listenBtnEvent();
    self.listenRegisterEvent();
    self.listenLoginEvent();
    self.listenEditEvent();
};

Login.prototype.listenRegisterEvent = function () {
    let self = this;
    let registerBtn = $('.register-btn');
    registerBtn.click(function (event) {
        event.preventDefault();
        let telephone = $("input[id='register-telephone']").val();
        let username = $("input[id='register-username']").val();
        let password1 = $("input[id='register-pwd1']").val();
        let password2 = $("input[id='register-pwd2']").val();
        blogajax.post({
            'url': '/blog/register/',
            // 'async' : false,
            'data': {
                'telephone': telephone,
                'username': username,
                'password1': password1,
                'password2': password2,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    window.messageBox.showSuccess('注册成功！');
                    window.location = window.location.href;
                } else {
                    window.messageBox.showError(result['message']);
                }
            }
        });
    });
};


Login.prototype.listenLoginEvent = function () {
    let self = this;
    let loginBtn = $(".login-btn");
    loginBtn.click(function (event) {
        event.preventDefault();
        let telephone = $("input[id='login-telephone']").val();
        let password = $("input[id='login-pwd']").val();
        let remember = $("input[name='remember']").prop('checked');
        blogajax.post({
            'url': '/blog/login/',
            'data': {
                'telephone': telephone,
                'password': password,
                'remember': remember ? 1 : 0, //三目运算符根据返回的结果判断，有就是1 没有就是0
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    window.messageBox.showSuccess('登录成功！');
                    window.location = window.location.href;
                } else {
                    window.messageBox.showError(result['message']);
                }
            }
        });
    });
};

Login.prototype.listenEditEvent = function () {
    let self = this;
    let editBtn = $(".edit-btn");
    editBtn.click(function (event) {
        event.preventDefault();
        let telephone = $("input[id='edit-telephone']").val();
        let old_pwd = $("input[id='old-pwd']").val();
        let new_pwd1 = $("input[id='new-pwd1']").val();
        let new_pwd2 = $("input[id='new-pwd2']").val();
        blogajax.post({
            'url': '/blog/personal/',
            'data': {
                'telephone': telephone,
                'old_pwd': old_pwd,
                'new_pwd1': new_pwd1,
                'new_pwd2': new_pwd2,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    window.location = window.location.href;
                    window.messageBox.showSuccess('修改成功！');
                } else {
                    window.messageBox.showError(result['message']);
                }
            }
        });
    });
};

$(function () {
    let login = new Login();
    login.run();
});