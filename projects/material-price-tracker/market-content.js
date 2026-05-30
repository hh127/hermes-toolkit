// 旗舰商家推荐
function FLAGSHOP() {}
FLAGSHOP.prototype = {
	init: function() {

		var marke = document.getElementsByName("tableId");
		var tableId = marke[0].content
		if(tableId == '85689'&& new Date().getTime()<=new Date('2025/11/05').getTime()){
			return
		}

		this.getShopUrl()
		this.renderFlagshop()
	},
	data: {
		cityId: jQuery('meta[name="cityId"]').attr('content') || '',
		cityName: jQuery('meta[name="cityName"]').attr('content') || '',
		breedId: jQuery('meta[name="breedId"]').attr('content') || '',
		breedShop: '',
		breedShops: ['010101', '010102', '010103', '010104', '010105', '010107', '010108', '010109', '010110',
			'010213', '010218', '0102'
		].sort().reverse(),
		breedShopsExclude: ['010216'] //排除不锈钢
	},
	getShopUrl: function() {
		// 对焊接钢筋网片品种单独处理
		if(this.data.breedId=='01010105'){
			this.data.breedShop = '010110'
		}else{
			// 判断是否为商铺品种，并找到商铺品种
			for (var i = 0; i < this.data.breedShops.length; i++) {
				if (this.data.breedId.indexOf(this.data.breedShops[i]) == 0) {
					this.data.breedShop = this.data.breedShops[i]
					//排除过滤的品种商铺
					for (var j = 0; j < this.data.breedShopsExclude.length; j++) {
						if (this.data.breedId.indexOf(this.data.breedShopsExclude[j]) == 0) {
							this.data.breedShop = ''
						}
					}
					break
				}
			}
		}
		var url = "//e.mysteel.com/vipshop/?breedId=" + this.data.breedShop + "&cityId=" + this.data.cityId
		$('.sososteel-vipshop-box-more').attr('href', url)
	},
	getFlagshopSpot: function(obj) {
		return $.ajax({
			url: 'https://e.mysteel.com/api/shop/flagship/queryFlagshipSpotHq',
			data: obj,
			type: 'get',
			async: false,
			timeout: 10000,
		})
	},
	renderFlagshop: function() {
		this.getFlagshopSpot({
			breedId: this.data.breedShop,
			areaCode: this.data.cityId,
			areaName: this.data.cityName,
		}).then(function(data) {
			if (data && data.data && data.data.length) {
				$('.sososteel-vipshop-box').show()
			}else{
				return
			}
			for (var i = 0; i < data.data.length; i++) {
				var price = data.data[i].telDiscuss ? '价格电议' : data.data[i].taxPrice + data.data[i]
					.taxPriceUnit
				var markDisplay = data.data[i].spotTrue ? "block" : "none"
				$('.sososteel-vipshop-box-main').append('<li class="sososteel-vipshop-box-main-item">' +
					'<a href="https://e.mysteel.com/ID' + (data.data[i].memberId||0) +
					'" target="_blank">' + '<div class="sososteel-vipshop-box-main-item-content">' +
					'<span class="sososteel-vipshop-box-main-item-content-mark" style="display:' +
					markDisplay + '">一级代理</span>' + '<img src="' + data.data[i].picUrl +
					'" alt="">' + '<p class="sososteel-vipshop-box-main-item-content-price">' +
					price + '</p>' + '</div>' +
					'<div class="sososteel-vipshop-box-main-item-info">' +
					'<div class="sososteel-vipshop-box-main-item-info__des">' +
					'<p class="ellipsis-1">' + data.data[i].resourceName + '</p>' +
					'<p class="ellipsis-1">' + data.data[i].companyName + '</p>' +
					'<div class="sososteel-vipshop-box-main-item-info__mark">' +
					'<img src="data:image/png;base64,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" alt="" class="icon icon-qj">' +
					'<img src="data:image/png;base64,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" alt="" class="icon icon-qy">' +
					'</div>' + '</div>' +
					'<div class="sososteel-vipshop-box-main-item-info__mark"></div>' + '</div>' +
					'</a>' + '</li>')
			}
		})
	}
}
var sososteelVipshop = new FLAGSHOP()
sososteelVipshop.init()

// 慧能学院
function HUINENGCOLLEGE() {}
HUINENGCOLLEGE.prototype = {
	init: function() {
		this.renderschool()
	},
	slide: function() {
		$('.school-box-main').slide({
			mainCell: '.school-list',
			titCell: '.school-dot p',
			effect: 'leftLoop',
			autoPlay: true,
			interTime: 3000
		})
	},
	renderschool: function() {
		var self = this
		$.ajax({
			type: 'post',
			url: '//openapi.mysteel.com/manual/queryPicNewsBySiteIds',
			data: JSON.stringify([
				[12644]
			]),
			timeout: '20000',
			headers: {
				"Content-Type": "application/json"
			},
			success: function(data) {
				var liveStr = ''
				if (data.length) {
					$('.school-box').show()
				}
				for (var i = 0; i < data.length; i++) {
					var targetA = data[i].targetUrl?
					'<a class="school-list-item" href="' + data[i].targetUrl +'" target="_blank" rel="nofollow">':
					'<a class="school-list-item" href="javascript:;" rel="nofollow">'
					liveStr += targetA
					liveStr += '    <img class="school-list-item-banner"    src="' + data[i]
						.imageUrl + '">'
					liveStr += '<div class="school-list-item-area">'
					liveStr += '<p class="school-list-title ellipsis-1" title="' + data[i].title +
						'">' + data[i].title + '</p>'
					liveStr += '    </div>'
					liveStr += '</a>'
					$('.school-dot').append('<p></p>')
				}
				$('.school-list').html(liveStr)
				if (data.length > 1) {
					self.slide()
				}
			},
			error: function(e) {
				console.log(e)
			}
		})
	},
}
var huinengCollege = new HUINENGCOLLEGE()
huinengCollege.init()

// 视频直播
function VIDEOLIVE() {}
VIDEOLIVE.prototype = {
	init: function() {
		// 检查.live-list里是否有数据
		if ($('.live-list').children().length > 0) {
			// 若有数据，显示.video-live-box
			$('.video-live-box').show();
			// 调用轮播方法
			this.slide();
		} else {
			// 若无数据，隐藏.video-live-box
			$('.video-live-box').hide();
		}
	},
	slide: function() {
		$('.video-live-box').slide({
			mainCell: '.live-list',
			titCell: '.list-list-dot p',
			effect: 'leftLoop',
			autoPlay: true,
			interTime: 3000
		})
	}
};
var videoLive = new VIDEOLIVE()
videoLive.init()

// 推荐经销商
function DEALERS() {}
DEALERS.prototype = {
	init: function() {
		var tableId = jQuery('meta[name="tableId"]').attr('content') || ''
		this.renderDealers({
			tableId: tableId
		})
	},
	renderDealers: function(obj) {
		$.ajax({
			type: 'get',
			url: '//api.mysteel.com/publishd/information/listDealer',
			data: obj,
			scriptCharset: 'utf-8',
			timeout: '20000',
			success: function(data) {
				if (data && data.response && data.response.length) {
					$('.market-dealers-box').show()
					var result = data.response
					for (var i = 0; i < result.length; i++) {
						if (result[i].url) {
							$('.market-dealers-box-ul').append(
								'<li class="market-dealers-box-item">' +
								'<a href="' + result[i].url + '" target="_blank">' + result[i].memberName +'</a>' +
								'</li>')
						} else {
							$('.market-dealers-box-ul').append(
								'<li class="market-dealers-box-item ellipsis-1">' + result[i].memberName + 
								'</li>'
							)
						}

					}
				}
				if ($(".market-dealers-box-ul li").length > 5) {
					$('.market-dealers-box').slide({
						mainCell: '.market-dealers-con ul',
						autoPlay: true,
						effect: 'topMarquee',
						vis: 5,
						scroll: 1,
						interTime: 80
					})
				}
			},
			error: function(e) {
				console.log(e)
			}
		})
	}
}
var dealer = new DEALERS()
dealer.init()

//周月均价
function PRICE() {}
PRICE.prototype = {
	init: function() {
		var tableId = jQuery('meta[name="tableId"]').attr('content') || '';
		var typeId = jQuery('meta[name="typeId"]').attr('content') || '';
		var breedId = jQuery('meta[name="breedId"]').attr('content') || '';
		var cityId = jQuery('meta[name="cityId"]').attr('content') || '';
		// 渲染周均价
		this.renderPriceDom({
			dom: $('#price-list-week'),
			typeIds: typeId,
			breedIds: breedId,
			relationType: "0",
			relationIds: cityId,
			type: 1
		})
		// 渲染月均价
		this.renderPriceDom({
			dom: $('#price-list-month'),
			typeIds: typeId,
			breedIds: breedId,
			relationType: "0",
			relationIds: cityId,
			type: 2
		})
	},
	fetchPrice: function(obj) {
		return $.ajax({
			url: '//api.mysteel.com/publishd/information/listMarketAvg',
			data: obj,
			type: 'get',
			async: false,
			timeout: 10000
		})
	},
	isToday: function(str) {
		return (new Date(str).toDateString() === new Date().toDateString())
	},
	isCurrentYear: function(str) {
		return (new Date(str).getFullYear() === new Date().getFullYear())
	},
	renderPriceDom: function(obj) {
		_this = this
		this.fetchPrice({
			typeIds: obj.typeIds || '',
			avgType: obj.type || '',
			//均价类型,1周、2月
			size: obj.size || 5,
			breedIds: obj.breedIds || '',
			relationType: obj.relationType || '',
			//relationType 关联类型(0 city、1 port、2 factory)
			relationIds: obj.relationIds || ''

		}).then(function(data) {
			if (data && data.response.length) {
				var result = data.response
				for (var i = 0; i < result.length; i++) {
					
					var timeClass = result[i].currentDay=='0' ? 'red' : ''
					var yearClass = result[i].currentYear=='0'? '' : 'past'
					obj.dom.append('<li class="' + yearClass + '">' + 
						'<span class="' + timeClass +'">[' + result[i].time6 + ']</span>' + 
						'<a href="' + result[i].pcUrl +'" title="' + result[i].title + '" target="_blank">' + result[i].title +'</a>'+ 
						'</li>')
				}
			} else {
				var parent =  obj.dom.closest('.column-box')
				var items = parent.find('.column-item')
				var	current = obj.dom.closest('.column-item')
				var currentIndex = items.index(current)
				parent.find('.column-btn-tab a').eq(currentIndex).attr('href','javascript:;').attr('target','')
				obj.dom.closest('.column-item').html(
					"<div class='no-data' style='display:block;'><i></i><p>暂无相关信息！</p>")
			}
		})
	}
}
new PRICE().init()
