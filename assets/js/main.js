$(document).ready(function () {

    // quick search regex
    var qsRegex;

    var $grid = $('.filterable').isotope({
        // options
        itemSelector: '.filter-item',
        percentPosition: true,
        layoutMode: 'fitRows',
        filter: function() {
            return qsRegex ? $(this).text().match( qsRegex ) : true;
        }
    });

// filter functions
    var filterFns = {
        // show if number is greater than 50
        numberGreaterThan50: function () {
            var number = $(this).find('#fee').val();
            console.log(number);
            return number > 500;
        },
        // show if name ends with -ium
        ium: function () {
            var name = $(this).find('.name').text();
            return name.match(/ium$/);
        }
    };

// bind filter button click
    $('.filters-button-group').on('click', 'button', function () {
        var filterValue = $(this).attr('data-filter');
        // use filterFn if matches value

        filterValue = filterFns[filterValue] || filterValue;
        $grid.isotope({filter: filterValue});
    });

    // use value of search field to filter
    var $quicksearch = $('.quicksearch').keyup( debounce( function() {
        qsRegex = new RegExp( $quicksearch.val(), 'gi' );
        $grid.isotope();
    }, 200 ) );

// debounce so filtering doesn't happen every millisecond
    function debounce( fn, threshold ) {
        var timeout;
        threshold = threshold || 100;
        return function debounced() {
            clearTimeout( timeout );
            var args = arguments;
            var _this = this;
            function delayed() {
                fn.apply( _this, args );
            }
            timeout = setTimeout( delayed, threshold );
        };
    }

});