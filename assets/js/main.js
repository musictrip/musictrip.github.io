$(document).ready(function () {

    // TODO Comment
    const fuseOptions = {
        shouldSort: true,
        includeScore: true,
        threshold: 0.55,
        location: 0,
        distance: 100,
        maxPatternLength: 32,
        minMatchCharLength: 1,
        keys: ["text", "fee", "instruments"]
    };


    // Holds the regex for free text search
    var searchInput;
    // Remember which filters are currently chosen in the button fields
    var chosenFilters = {};

    var $grid = $('.filterable').isotope({
        // options
        itemSelector: '.filter-item',
        percentPosition: true,
        layoutMode: 'fitRows',
        filter: function () {
            // Does the current item match the search?
            if (searchInput) {
                var strippedText = $(this).text().replace(/\s/g, '');

                var searchDict = [{
                    "text": strippedText,
                    "fee": $(this).find("#fee").val().toString(),
                    "instruments": $(this).find("#instruments").val(),
                }];


                var fuse = new Fuse(searchDict, fuseOptions);
                var fuseResult = fuse.search(searchInput);
                searchResult = fuseResult.length > 0;

            } else {
                searchResult = true;
            }


            // Check if the current element satisfies all button criteria
            var selectionResults = concatValues(chosenFilters)
                .map(x => $(this).is(x))
                .every(x => x);


            return searchResult && selectionResults;
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
        searchInput = $quicksearch.val();

        $grid.isotope();
    }, 200));


    $(".filters-select").on("change", function () {
        var filterValue = $(this).val();

        chosenFilters["instruments"] = filterValue;

    });


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


    // Activate select2 selector
    $(document).ready(function () {
        $(".select2-selector").select2({
            placeholder: '選樂器　'
        });
    });

});
