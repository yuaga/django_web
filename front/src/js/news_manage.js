function News_manage() {

}


News_manage.prototype.initDatePicker = function () {
    let startTime = $("#starttime");
    let endTime = $("#endtime");
    let options = {
        'showButtonPanel': true,  // 是否有按钮
        'format': 'yyyy/m/d',   //格式化日期格式
        'language': 'zh-CN',   //  设置语言
        'todayHighlight': true,  // 将今日设为高亮
        'clearBtn': true,  // 设置清除按钮
        'autoclose': true  //  当选定日期后，日期框自动关闭
    };
    startTime.datepicker(options);  // 里面不传参数就是默认的样式
    endTime.datepicker(options);
};


News_manage.prototype.ListenDelEvent = function () {
    let self = this;
    let delBtn = $('.delete-btn');
    delBtn.click(function () {
        let currentBtn = $(this);
        let pk = currentBtn.attr('data-news-id');
        blogalert.alertConfirm({
            'title': '确认删除吗？',
            'confirmCallback': function () {
                // console.log('pp');
                blogajax.post({
                    'url': '/cms/del_news/',
                    'data': {
                        'pk': pk,
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.location = window.location.href;
                            // window.location.reload(); 兼容性不好
                        } else {
                            blogalert.close();
                        }
                    }
                });
            }
        });
    });
};

News_manage.prototype.run = function () {
    let self = this;
    self.initDatePicker();
    self.ListenDelEvent();
};


$(function () {
    let newsManage = new News_manage();
    newsManage.run();
});