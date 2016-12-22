import React from "react";
require("../js/bootstrap.min");
var Header = React.createClass({
    componentDidMount(){
        $("#nav_nav>ul>li").on("click",function () {
            $(this).addClass("active").siblings().removeClass("active");
        });
        var hash = location.hash;
        $("#nav_nav>ul>li").each(function () {
            if(hash.indexOf($(this).attr("data-hash"))>-1){
                $("#nav_nav>ul>li").removeClass("active");
                $(this).addClass("active");
                return;
            }
        });
    },
    render:function () {
        return <nav className="navbar navbar-default" role="navigation">
            <div className="container-fluid">
                <div className="navbar-header">
                    <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#nav_nav">
                        <span className="sr-only">Toggle navigation</span>
                        <span className="icon-bar"> </span>
                        <span className="icon-bar"> </span>
                        <span className="icon-bar"> </span>
                    </button>
                    <a className="navbar-brand" href="#/">PSMS</a>
                </div>

                <div className="collapse navbar-collapse" id="nav_nav">
                    <ul className="nav navbar-nav">
                        <li data-hash="customer" className="dropdown active">
                            <a href="javascript:void(0)" className="dropdown-toggle" data-toggle="dropdown">Advertiser <span className="caret"></span></a>
                            <ul className="dropdown-menu" role="menu">
                                <li><a href="#/create_customer">Create Customer</a></li>
                                <li className="divider"> </li>
                                <li><a href="#/customer_list">Customer List</a></li>
                            </ul>
                        </li>
                        <li data-hash="offer" className="dropdown">
                            <a href="javascript:void(0)" className="dropdown-toggle" data-toggle="dropdown">Offer <span className="caret"></span></a>
                            <ul className="dropdown-menu" role="menu">
                                <li><a href="#/create_offer">Create Offer</a></li>
                                <li className="divider"> </li>
                                <li><a href="#/offer_list">Offer List</a></li>
                            </ul>
                        </li>
                        <li><a href="#/about">About</a></li>
                        <li><a href="#/list">List</a></li>
                    </ul>
                    {/*<ul className="nav navbar-nav navbar-right">
                        <li><a href="#">Link</a></li>
                        <li className="dropdown">
                            <a href="#" className="dropdown-toggle" data-toggle="dropdown">Dropdown <span className="caret"></span></a>
                            <ul className="dropdown-menu" role="menu">
                                <li><a href="#">Action</a></li>
                                <li><a href="#">Another action</a></li>
                                <li><a href="#">Something else here</a></li>
                                <li className="divider"></li>
                                <li><a href="#">Separated link</a></li>
                            </ul>
                        </li>
                    </ul>*/}
                </div>
            </div>
        </nav>

    }
});
module.exports = Header;
