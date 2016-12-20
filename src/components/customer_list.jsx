import React from "react";

var CustomerList = React.createClass({
    render:function () {
        return (
            <div>
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
                    <table className="table table-bordered">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>客户编码</th>
                                <th>客户名称</th>
                                <th>公司名称</th>
                                <th>公司地址</th>
                                <th>操作</th>
                                <th>最后修改</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>1000</td>
                                <td>R30025</td>
                                <td>Table cell Table cell客户名称</td>
                                <td>Table cell Table cell公司名称</td>
                                <td>Table cell Table cell公司地址</td>
                                <td><a href="#/create_customer/(:id)" className="btn btn-primary">Edit</a></td>
                                <td>2016-12-06 18:34</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        )
    }
});
export default  CustomerList;
