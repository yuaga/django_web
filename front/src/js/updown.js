function UpDwn() {

}


UpDwn.prototype.listenUpEvent = function () {
    let self = this;
    let upBtn = $('.up');
    upBtn.click(function () {
        let btn = $(this);
        let news_id = btn.parent().attr('data-news-id');
        let up = btn.attr('data-up');
        blogajax.post({
            'url': '/news/up/',
            'data': {
                'news_id': news_id,
                'up': up
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    window.messageBox.showSuccess(result['message']);
                    window.location = window.location.href;
                }
            }
        });
    });
};

UpDwn.prototype.listenDownEvent = function () {
    let self = this;
    let upBtn = $('.down');
    upBtn.click(function () {
        console.log('1111');
        let btn = $(this);
        let news_id = btn.parent().attr('data-news-id');
        let down = btn.attr('data-up');
        blogajax.post({
            'url': '/news/down/',
            'data': {
                'news_id': news_id,
                'down': down
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    window.messageBox.showSuccess(result['message']);
                    window.location = window.location.href;
                    console.log(news_id);
                }
            }
        });
    });
};

UpDwn.prototype.run = function () {
    let self = this;
    self.listenUpEvent();
    self.listenDownEvent();
};


$(function () {
    let news = new UpDwn();
    news.run();
});
