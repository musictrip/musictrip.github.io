$(document).ready(function () {

    // TODO Comment


    // Holds the regex for free text search
    var qsRegex;
    // Remember which filters are currently chosen in the button fields
    var chosenFilters = {};

    var $grid = $('.filterable').isotope({
        // options
        itemSelector: '.filter-item',
        percentPosition: true,
        layoutMode: 'fitRows',
        filter: function () {
            // Does the current item match the free search regex?
            var searchResult = qsRegex ? $(this).text().match(qsRegex) : true;

            // Check if the current element satisfies all button criteria
            var buttonResult = concatValues(chosenFilters)
                .map(x => $(this).is(x))
                .every(x => x);

            return searchResult && buttonResult;
        }
    });

// filter functions
    var filterFns = {
        // show if number is greater than 500
        feeBelow500Euro: function () {
            var fee = $(this).find('#fee').val();
            return fee < 500;
        },
        fee500to1000Euro: function () {
            var fee = $(this).find('#fee').val();
            return fee >= 500 && fee < 1000;
        },
        feeAbove1000Euro: function () {
            var fee = $(this).find('#fee').val();
            return fee > 1000;
        },

    };

// bind filter button click
    $('.filters-button-group').on('click', 'button', function (event) {
        var $button = $(event.currentTarget);
        var $buttonGroup = $button.parents('.button-group');
        var $filterGroup = $buttonGroup.attr('data-filter-group');


        var newFilter = filterFns[$button.attr('data-filter')] || $button.attr('data-filter');
        if (chosenFilters.hasOwnProperty($filterGroup)) {
            if (chosenFilters[$filterGroup] === newFilter) {
                $buttonGroup.find('.is-checked').removeClass('is-checked');
                delete chosenFilters[$filterGroup];
            } else {
                $buttonGroup.find('.is-checked').removeClass('is-checked');
                $button.addClass('is-checked');
                chosenFilters[$filterGroup] = newFilter;
            }


        } else {
            $button.addClass('is-checked');
            chosenFilters[$filterGroup] = newFilter;
        }

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
    function concatValues(dict) {
        return Object.values(dict);
    }

});