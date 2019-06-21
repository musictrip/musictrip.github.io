$(document).ready(function () {

    // TODO Comment

    // quick search regex
    var qsRegex;
    var buttonFilter = [];
    var chosenFilters = {};

    var $grid = $('.filterable').isotope({
        // options
        itemSelector: '.filter-item',
        percentPosition: true,
        layoutMode: 'fitRows',
        filter: function () {
            var searchResult = qsRegex ? $(this).text().match(qsRegex) : true;

            console.log("buttonFilter in individual call", buttonFilter);
            buttonResults = buttonFilter.map(x =>  $(this).is(x));
            console.log("buttonResults", buttonResults);
            var buttonResult = buttonResults.every(x => x);
            console.log(buttonResult);
            return searchResult && buttonResult;
        }
    });

// filter functions
    var filterFns = {
        // show if number is greater than 50
        numberGreaterThan50: function () {
            var number = $(this).find('#fee').val();
            return number > 500;
        },

    };

// bind filter button click
    $('.filters-button-group').on('click', 'button', function (event) {
        var $button = $(event.currentTarget);
        var $buttonGroup = $button.parents('.button-group');
        var filterGroup = $buttonGroup.attr('data-filter-group');
        chosenFilters[filterGroup] = filterFns[$button.attr('data-filter')] || $button.attr('data-filter');


        buttonFilter = concatValues(chosenFilters);

        $grid.isotope();
    });


    // use value of search field to filter
    var $quicksearch = $('.quicksearch').keyup(debounce(function () {
        qsRegex = new RegExp($quicksearch.val(), 'gi');
        $grid.isotope();
    }, 200));


// debounce so filtering doesn't happen every millisecond
    function debounce(fn, threshold) {
        var timeout;
        threshold = threshold || 100;
        return function debounced() {
            clearTimeout(timeout);
            var args = arguments;
            var _this = this;

            function delayed() {
                fn.apply(_this, args);
            }

            timeout = setTimeout(delayed, threshold);
        };
    }

    // flatten object by concatting values
    function concatValues(obj) {
        var values = [];
        for (const prop in obj) {
            values.push(obj[prop]);
        }
        return values;
    }


});