function formatSearchResult(entity) {
    var singleResult = '<div>' + entity.name + ' <span class="entity-type">' + entity.type;

    if (entity.type == "sensor") {
        singleResult += ' (' + entity.host + ')';
    }

    if (entity.type == "metric") {
        singleResult += ' (' + entity.host + ' &raquo; ' + entity.sensor + ')';
    }

    singleResult += '</div>'

    return singleResult;
}

function formatSearchSelection(entity) {
    return entity.name;
}

$(document).ready(function() {
    $("#search").select2({
        width: "element",
        placeholder: "Search...",
        minimumInputLength: 2,
        ajax: { 
            url: "/search",
            dataType: 'json',
            data: function (term, page) {
                return {
                    s: term
                };
            },
            results: function (data, page) { 
                return {results: data};
            }
        },
        initSelection: function(element, callback) {
            var id=$(element).val();
        }, 
        id: function(entity) { return entity.name; }, // Be careful, it may cause problems - names aren't unique
        formatResult: formatSearchResult,
        formatSelection: formatSearchSelection,
        escapeMarkup: function (m) { return m; }
    });
});