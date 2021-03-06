$(document).ready(function () {

    const fuseOptions = {
        shouldSort: true,
        includeScore: true,
        threshold: 0.2,
        location: 0,
        distance: 10000,
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

                // The instrument name does not need to be normalized as it is already in Chinese
                var instrument = $(this).find("#instruments").val();
                instrument += englishNameOf(instrument);

                var searchDict = [{
                    "text": $(this).find('#hiddenText').val(),
                    "fee": $(this).find("#fee").val().toString(),
                    "instruments": instrument,
                }];

                var fuse = new Fuse(searchDict, fuseOptions);
                var normalizedSearchInput = normalizeString(searchInput);
                var fuseResult = fuse.search(normalizedSearchInput);

                searchResult = fuseResult.length > 0;

            } else {
                searchResult = true;
            }

            // Check if the current element satisfies all button criteria
            var selectionResults = getSelectionResults($(this), chosenFilters);

            return searchResult && selectionResults;
        }
    });

    /**
     * The following two functions are there to keep the search input when leaving and returning to the page.
     *
     * In the first function we save the old search input in the browsers local storage.
     * The second function checks if there is old search input and reloads it if appropriate.
     *
     */
    $("#search-bar").bind("input", function () {
        input = $(this).val();
        localStorage.setItem("search-bar-input", input);
    });
    $(document).ready(function () {
        oldSearchInput = localStorage.getItem("search-bar-input");
        searchBar = $("#search-bar");

        if (oldSearchInput) {
            searchInput = oldSearchInput;
            $grid.isotope();
        }

        // Check whether the search bar is not focussed
        // We do not want to reset the search input if the search bar is focussed, because then it is impossible to fully
        // delete the text in the input field
        if (!searchBar.is(":focus")) {
            // Set the searchInput variable to the right value (this is the variable we use for filtering in isotope).
            searchBar.focus();
            searchBar.val(oldSearchInput);
        }
    });


    /**
     * Translate Chinese instrument names to english
     * @param s Chinese instrument name
     * @returns {string} English translation of Chinese instrument name
     */
    function englishNameOf(s) {
        switch (s) {
            case "大提琴":
                return "cello";
            case "中提琴":
                return "viola";
            case "小提琴":
                return "violin";
            case "低音提琴":
                return "bass";
            case "鋼琴":
                return "piano";
            case "打擊樂":
                return "percussion, drums";
            case "聲樂":
                return "vocal, singing";
            case "指揮":
                return "conductor";
            case "長笛":
                return "western concert flute";
            case "雙簧管":
                return "oboe";
            case "單簧管":
                return "clarinet";
            case "低音管":
                return "bassoon";
            case "法國號":
                return "french horn";
            case "小號":
                return "trumpet";
            case "長號":
                return "trombone";
            case "低音號":
                return "tuba";
            default:
                return "";
        }
    }

    /**
     * Normalize a string
     * That is, replace all its whitespace
     * @param s input string
     * @returns string string with all whitespace removed
     */
    function normalizeString(s) {
        return s.toLowerCase().replace(/\s+/g, '');
    }


    /**
     * TODO
     * @param masterclassCard
     * @param chosenFilters
     */
    function getSelectionResults(masterclassCard, chosenFilters) {

        if ("instruments" in chosenFilters) {
            const chosenInstrument = chosenFilters["instruments"];
            const cardInstruments = masterclassCard.find("#instruments").val();
            var instrumentContained = cardInstruments.includes(chosenInstrument);

            if (!instrumentContained) {
                return false;
            }
        }

        if ("fee" in chosenFilters) {

            const masterclassFee = masterclassCard.find("#fee").val();
            const range = chosenFilters["fee"];

            if (masterclassFee < parseFloat(range["from"]) || masterclassFee > parseFloat(range["to"])) {
                return false;
            }
        }

        if ("type" in chosenFilters) {
            if (!masterclassCard.is(chosenFilters["type"])) {
                return false;
            }
        }

        return true;
    }


// filter functions
    var filterFns = {
        // show if number is greater than 500
        feeBelow500Euro: function (masterclassCard) {
            var fee = masterclassCard.find('#fee').val();
            return fee < 500;
        },
        fee500to1000Euro: function (masterclassCard) {
            var fee = masterclassCard.find('#fee').val();
            return fee >= 500 && fee < 1000;
        },
        feeAbove1000Euro: function (masterclassCard) {
            var fee = masterclassCard.find('#fee').val();
            return fee > 1000;
        },

    };

    /**
     * TODO
     */
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

    /**
     * Reset chosen filters when expanded search is collapsed
     */
    $("#collapseExample").on("hidden.bs.collapse", function () {
        // Clear chosen filters
        chosenFilters = {};

        // Clear search button, select field and slider
        $(".filters-button").removeClass("is-checked");
        $('.filters-select').val(null).trigger('change');
        slider.noUiSlider.set([sliderStartValue, sliderEndValue]);

        // Show all items
        $grid.isotope();

    });


    // use value of search field to filter
    var $quicksearch = $('.quicksearch').keyup(debounce(function () {
        searchInput = $quicksearch.val();

        $grid.isotope();
    }, 200));

    /**
     * TODO
     */
    $(".filters-select").on("change", function () {
        var filterValue = $(this).val();
        chosenFilters["instruments"] = filterValue;
        $grid.isotope();
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
            placeholder: '---',
            allowClear: true
        });
    });

    var slider = document.getElementById('feeSlider');
    const sliderStartValue = 0;
    const sliderEndValue = 1500
    noUiSlider.create(slider, {
        start: [sliderStartValue, sliderEndValue],
        step: 50,
        range: {
            'min': sliderStartValue,
            'max': sliderEndValue
        },
        margin: 100,
        tooltips: true,
        format:
            {
                from: Number,
                to: function (value) {
                    return (parseInt(value) + " €");
                }
            }

    });


    slider.noUiSlider.on('update', function (values) {
        chosenFilters["fee"] = {from: values[0], to: values[1]};

        $grid.isotope();
    });


});


new WOW().init();
