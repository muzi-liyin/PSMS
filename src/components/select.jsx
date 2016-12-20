import React from "react";
require("select2");
require("select2/dist/css/select2");

var Select = React.createClass({
    componentDidMount(){
        var data = [{ id: 0, text: 'enhancement' }, { id: 1, text: 'bug' }, { id: 2, text: 'duplicate' }, { id: 3, text: 'invalid' }, { id: 4, text: 'wontfix' }];

        $(".js-example-data-array").select2({
            data: data
        })
    },
    render(){
        return (
            <select className="js-example-data-array"></select>
        )
    }
});

var AjaxSelect = React.createClass({
    componentDidMount(){
        $(".js-data-example-ajax").select2({
            ajax: {
                url: "https://api.github.com/search/repositories",
                dataType: 'json',
                delay: 1000,
                data: function (params) {
                    return {
                        q: params.term,
                        page: params.page
                    };
                },
                processResults: function (data, params) {
                    var data = [{ id: 0, text: 'enhancement' }, { id: 1, text: 'bug' }, { id: 2, text: 'duplicate' }, { id: 3, text: 'invalid' }, { id: 4, text: 'wontfix' }];

                    params.page = params.page || 1;
                    return {
                        results: data
                    };
                },
                cache: true
            },
            minimumInputLength: 1
        });
    },
    render(){
        return (
            <select className="js-data-example-ajax">
                <option defaultValue="3620194" >select2/select2</option>
            </select>
        )
    }
});

module.exports ={
    Select:Select,
    AjaxSelect:AjaxSelect
}
