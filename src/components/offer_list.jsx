import React from "react";

var OfferList = React.createClass({
    render:function () {
        return (
            <div id="offer_list">
                <div className="row">
                    <div className="col-md-8">&nbsp;</div>
                    <div className="form-group col-md-4 text-right">
                        <div className="input-group">
                            <div className="input-group-addon">Export</div>
                            <input className="form-control" type="email" placeholder="Search..." />
                            <div className="input-group-addon">Search</div>
                        </div>
                    </div>
                </div>
                <div className="table-responsive">
                    <table className="table table-bordered text-center">
                        <thead>
                            <tr>
                                <th>Status</th>
                                <th>Offer ID</th>
                                <th>应用名称</th>
                                <th>系统</th>
                                <th>客户名称</th>
                                <th>合作模式</th>
                                <th>投放地区</th>
                                <th>单价</th>
                                <th>投放起始</th>
                                <th>投放截止</th>
                                <th>操作</th>
                                <th>最后修改</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>
                                    <div className="isTrue"></div>
                                </td>
                                <td><a href="#/offer_detail/1000">1000</a></td>
                                <td>应用名称</td>
                                <td>系统</td>
                                <td>客户名称</td>
                                <td>合作模式</td>
                                <td>投放地区</td>
                                <td>单价</td>
                                <td>投放起始</td>
                                <td>投放截止</td>
                                <td>
                                    <img src="./src/img/zx.jpg"/> <a href="#/create_offer/(:id)" className="btn btn-primary">Edit</a>
                                </td>
                                <td>最后修改</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        )
    }
});
export default  OfferList;
