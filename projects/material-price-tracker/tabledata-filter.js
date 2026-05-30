function MarketTableDataFilter() {}

MarketTableDataFilter.prototype = {
  constructor: MarketTableDataFilter,
  filterData: [],
  init: function () {
    this.initFilterList()
    this.initSelectList()
    this.clickEvent()
  },
  // 数组去重
  uniqueArr: function (arr) {
    var list = []
    for (var i = 0; i < arr.length; i++) {
      if (list.indexOf(arr[i]) == -1) {
        list.push(arr[i])
      }
    }
    return list
  },
  // 初始化当前筛选的数据结构
  initFilterList: function () {
    var self = this
    $('.table-filter-select').each(function () {
      self.filterData.push({
        line: $(this).attr('sort-line-num'),
        name: $(this).attr('sort-line-name'),
        list: []
      })
    })
  },
  // 初始化获取筛选下拉列表
  initSelectList: function () {
    var self = this
    $('.table-filter-select').each(function () {
      var str = '',
        sortList = [],
        sortLine = $(this).attr('sort-line-num'),
        sortAlias = $(this).siblings().data('sort-alias')

      // 给靠右侧的筛选设置下拉列表位置
      if (sortLine > 5) {
        $(this).find('.table-filter-select-dropdown').addClass('dropdown-left')
      }

      $('#marketTable tbody tr td').each(function () {
        var text = String($(this).data('name')) || $(this).text()
        if (sortLine == $(this).index() + 1) {
          if (text.replace(/[\n\t\s]+/g, '')) {
            sortList.push(text.replace(/[\n\t\s]+/g, ''))
          }
        }
      })

      // 渲染下拉列表数据，数据为空时隐藏下拉列表
      var uniqueSortList = self.uniqueArr(sortList)

      if (sortAlias === 'place') {
        uniqueSortList.sort(function compareFunction(a, b) {
          if (a.slice(0, 1) == '长') {
            a = '唱' + a.split('').slice(1, a.split('').length).join('')
          }
          if (b.slice(0, 1) == '长') {
            b = '唱' + b.split('').slice(1, b.split('').length).join('')
          }
          return a.localeCompare(b)
        })
      }

      if (sortAlias === 'spec') {
        uniqueSortList.sort(function (a, b) {
          if (a.indexOf('Ф') > -1 || a.indexOf('Φ') > -1) {
            if (a.indexOf('>Φ') > -1 || a.indexOf('>Ф') > -1) {
              a = a.slice(2)
            } else {
              a = a.slice(1)
            }
          }
          if (b.indexOf('Ф') > -1 || b.indexOf('Φ') > -1) {
            if (b.indexOf('>Φ') > -1 || b.indexOf('>Ф') > -1) {
              b = b.slice(2)
            } else {
              b = b.slice(1)
            }
          }

          if (a.indexOf('φ') > -1 || a.indexOf('φ') > -1) {
            a = a.slice(1)
          }
          if (b.indexOf('φ') > -1 || b.indexOf('φ') > -1) {
            b = b.slice(1)
          }
          return parseFloat(a) - parseFloat(b)
        })
      }

      if (uniqueSortList.length) {
        for (var i = 0; i < uniqueSortList.length; i++) {
          str += '<li>' + uniqueSortList[i] + '</li>'
        }
        $(this).find('.table-filter-select-dropdown-list').html(str)
      } else {
        $(this).remove()
      }
    })
  },
  // 渲染当前筛选
  renderCurrentFilter: function () {
    var str = ''
    for (var i = 0; i < this.filterData.length; i++) {
      var data = this.filterData[i]
      if (data['list'].length) {
        str += '<strong class="blue">' + data['name'] + '：</strong>'
        for (var j = 0; j < data['list'].length; j++) {
          str +=
            '<p class="table-filter-selected-list-item" data-name="' +
            data['name'] +
            '" data-line="' +
            data['line'] +
            '">'
          str += '<span>' + data['list'][j] + '</span>'
          str +=
            '<img src="//a.mysteelcdn.com/common/3.0/images/delete-filter.png?v=20220930">'
          str += '</p>'
        }
      }
    }

    if (str) {
      $('.table-filter-selected-clear').show()
    } else {
      $('.table-filter-selected-clear').hide()
    }
    $('.table-filter-selected-list').html(str)

    this.renderFilterTableData()
  },
  // 渲染表格数据
  renderFilterTableData: function () {
    $('#marketTable tbody tr').each(function () {
      $(this).show()
    })

    for (var i = 0; i < this.filterData.length; i++) {
      var data = this.filterData[i]
      $('#marketTable tbody tr td').each(function () {
        var line = $(this).index() + 1

        // 判断索引和筛选组
        if (data['line'] == line && data['list'].length) {
          var text = String($(this).data('name')) || $(this).text()
          if (data['list'].indexOf(text.replace(/[\n\t\s]+/g, '')) == -1) {
            $(this).parent().hide()
          }
        }
      })
    }
    // this.initFilterSelectList()
  },
  // 渲染当前实时筛选的下拉列表
  initFilterSelectList: function () {
    var self = this
    $('.table-filter-select').each(function () {
      var str = '',
        sortList = [],
        sortLine = $(this).attr('sort-line-num')

      $('#marketTable tbody tr td').each(function () {
        var text = $(this).text(),
          isShow = $(this).parent().css('display') != 'none'

        if (sortLine == $(this).index() + 1 && isShow) {
          if (text.replace(/[\n\t\s]+/g, '')) {
            sortList.push(text.replace(/[\n\t\s]+/g, ''))
          }
        }
      })

      // 渲染下拉列表数据，数据为空时隐藏下拉列表
      var uniqueSortList = self.uniqueArr(sortList)
      if (uniqueSortList.length) {
        for (var i = 0; i < uniqueSortList.length; i++) {
          str += '<li>' + uniqueSortList[i] + '</li>'
        }
        $(this).find('.table-filter-select-dropdown-list').html(str)
      }
    })

    // 根据当前筛选设置下拉列表的选中效果
    $('.table-filter-select-dropdown-list li').each(function () {
      var text = $(this).text(),
        line = $(this).closest('.table-filter-select').attr('sort-line-num')

      for (var i = 0; i < self.filterData.length; i++) {
        var data = self.filterData[i]

        if (data['line'] == line && data['list'].indexOf(text) != -1) {
          $(this).addClass('active')
        }
      }
    })
  },
  reseDropdownStatus: function () {
    $('.table-filter-select-dropdown-search').val('')
    $('.table-filter-select-dropdown-list li').show()
  },
  clickEvent: function () {
    var self = this,
      flag = true,
      selectClassName = '.table-filter-select',
      dropdownClassName = '.table-filter-select-dropdown',
      inputClassName = '.table-filter-select-dropdown-search',
      liClassName = '.table-filter-select-dropdown-list li'

    // 鼠标移入显示筛选下拉框
    $('body').on('mouseenter', selectClassName, function () {
      var name = $(this).attr('sort-line-name')

      $(selectClassName).each(function () {
        if ($(this).attr('sort-line-name') == name) {
          $(this).find(dropdownClassName).show()

          // 如果下拉列表长度超出，显示省略号并且显示title
          try {
            $(this)
              .find(liClassName)
              .each(function () {
                if ($(this).get(0).scrollWidth > $(this).get(0).offsetWidth) {
                  $(this).addClass('text-ellipsis')
                  $(this).attr('title', $(this).text())
                }
              })
          } catch (error) {
            console.log(error)
          }
        } else {
          $(this).find(dropdownClassName).hide()
          $(this).find(inputClassName).val('')
          $(this).find(liClassName).show()
        }
      })
    })

    // 鼠标移出，如果输入框未聚焦，隐藏筛选下拉框
    $('body').on('mouseleave', selectClassName, function () {
      var status = $(this).find(inputClassName).is(':focus')

      if (!status) {
        $(this).find(dropdownClassName).hide()
      }
    })

    // 隐藏筛选下拉框
    $('body').click(function () {
      $(dropdownClassName).hide()
      self.reseDropdownStatus()
    })

    $('body').on('click', selectClassName, function (e) {
      e.stopPropagation()
      $(this).find(dropdownClassName).show()
    })

    // 筛选列表搜索事件
    $('body').on('compositionstart', inputClassName, function () {
      flag = false
    })

    // 筛选列表搜索事件
    $('body').on('compositionend', inputClassName, function () {
      flag = true
    })

    // 筛选列表搜索事件
    $('body').on('input', inputClassName, function () {
      var that = this

      setTimeout(function () {
        var searchText = $(that).val().trim()

        if (flag) {
          $(that)
            .closest(selectClassName)
            .find(liClassName)
            .each(function () {
              if (searchText) {
                if ($(this).text().indexOf(searchText) == -1) {
                  $(this).hide()
                } else {
                  $(this).show()
                }
              } else {
                $(this).show()
              }
            })
        }
      }, 100)
    })

    // 筛选列表点击事件
    $('body').on('click', liClassName, function (e) {
      e.stopPropagation()
      $(this).hasClass('active')
        ? $(this).removeClass('active')
        : $(this).addClass('active')

      var line = $(this).closest(selectClassName).attr('sort-line-num'),
        selectStatus = $(this).hasClass('active'),
        selectText = $(this).text()

      for (var i = 0; i < self.filterData.length; i++) {
        var data = self.filterData[i]

        // 匹配筛选列
        if (data['line'] == line) {
          selectStatus
            ? data['list'].push(selectText)
            : data['list'].splice(data['list'].indexOf(selectText), 1)
        }
      }

      self.renderCurrentFilter()
    })

    // 当前筛选删除事件
    $('body').on('click', '.table-filter-selected-list-item img', function () {
      var text = $(this).siblings().text(),
        line = $(this).parent().data('line')

      for (var i = 0; i < self.filterData.length; i++) {
        var data = self.filterData[i]

        // 匹配筛选列
        if (data['line'] == line) {
          data['list'].splice(data['list'].indexOf(text), 1)
        }
      }

      // 移除当前选中效果
      $(liClassName).each(function () {
        var selectText = $(this).text(),
          selectLine = $(this).closest(selectClassName).attr('sort-line-num')

        if (selectLine == line && selectText == text) {
          $(this).removeClass('active')
        }
      })

      self.renderCurrentFilter()
    })

    // 当前筛选清空事件
    $('body').on('click', '.table-filter-selected-clear', function () {
      for (var i = 0; i < self.filterData.length; i++) {
        self.filterData[i]['list'] = []
      }

      $(liClassName).each(function () {
        $(this).removeClass('active')
      })

      self.renderCurrentFilter()
    })
  }
}

new MarketTableDataFilter().init()
