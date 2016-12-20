import React from "react";
import {Router,Route,hashHistory,IndexRedirect} from "react-router";

import App from  '../components/app';
import About from "../components/about";
import List from "../components/list";
import Welcome from "../components/welcome";
import CreateCustomer from "../components/create_customer";
import CustomerList from "../components/customer_list";
import CreateOffer from "../components/create_offer";
import OfferList from "../components/offer_list";
import OfferDetail from "../components/offer_detail";


var Routers = <Router history={hashHistory}>
                <Route path="/"  component={App}>
                    <IndexRedirect to="/welcome" />
                    <Route path="/welcome" component={Welcome}/>

                    <Route path="/create_customer(/:id)" component={CreateCustomer}/>
                    <Route path="/customer_list" component={CustomerList}/>

                    <Route path="/create_offer(/:id)" component={CreateOffer}/>
                    <Route path="/offer_list" component={OfferList}/>
                    <Route path="/offer_detail/:id" component={OfferDetail}/>

                    <Route path="list(/:name)" component={List}/>
                    <Route path="about" component={About}/>
                </Route>
             </Router>

export default Routers;