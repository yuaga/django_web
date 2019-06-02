function CommentManage() {

}


CommentManage.prototype.run = function () {
    var self = this;
    self.listenDelCommentEvent();
};

CommentManage.prototype.listenDelCommentEvent = function () {
    var self = this;
    var delBtn = $('.delete-btn');
    delBtn.click(function () {
        var currentBtn = $(this);
        var pk = currentBtn.attr('data-pk');
        blogalert.alertConfirm({
            'title': '确认删除吗？',
            'confirmCallback': function () {
                blogajax.post({
                    'url': '/cms/del_comment/',
                    'data': {
                        'pk': pk,
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.location = window.location.href;
                        } else {
                            blogalert.close();
                        }
                    }
                });
            }
        });
    });
};

$(function () {
    var comment = new CommentManage();
    comment.run();
});