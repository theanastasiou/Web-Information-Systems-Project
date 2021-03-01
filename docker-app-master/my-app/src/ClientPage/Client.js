import React, { Component } from "react";
import { Button } from "react-bootstrap";
import history from "./../history";
import Dropdown from "react-dropdown";
import Select from "react-select";
import "react-dropdown/style.css";
import axios from "axios";
import "./Client.css";
import ReactDOM from "react-dom";
import Moment from "moment";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";

const Loader = () => (
  <div class="divLoader">
    <svg class="svgLoader" viewBox="0 0 100 100" width="10em" height="10em">
      <path
        stroke="none"
        d="M10 50A40 40 0 0 0 90 50A40 42 0 0 1 10 50"
        fill="#51CACC"
        transform="rotate(179.719 50 51)"
      >
        <animateTransform
          attributeName="transform"
          type="rotate"
          calcMode="linear"
          values="0 50 51;360 50 51"
          keyTimes="0;1"
          dur="1s"
          begin="0s"
          repeatCount="indefinite"
        ></animateTransform>
      </path>
    </svg>
  </div>
);
export default class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      options: [],
      slots: [],
      selectedId: "",
      selectedItem: "",
      date: new Date(),
      datetosend:"",
      userslots:[],
      userdates:[],
      userconfirmed:[],
      usercarrier:[]
    };
    this.baseState=this.state;
    // let user = localStorage.getItem('username');
    // ReactDOM.render(<p>Hallo {user}</p>,document.getElementById('header'));
    this.change = this.change.bind(this);
    this.calendarchange = this.calendarchange.bind(this);
   // this.submitappointment = this.submitappointment.bind(this);
    this.handleCalendarSubmit = this.handleCalendarSubmit.bind(this);
    this.getCarriers = this.getCarriers.bind(this);
    this.showapp = this.showapp.bind(this);
   
  }

  showapp(){
    axios.get('/appointments_userid/'+localStorage.getItem("userid"))
    .then(response => {
      console.log(response.data);
      this.setState({userslots:[]});
      this.setState({userdates:[]});
      this.setState({userconfirmed:[]});
      this.setState({usercarrier:[]});
      if(response.data.length != 0){
        console.log(response.data);
        console.log(response.data[0].number);
       
        console.log(this.state.slots+" must be nulllllllllllllllllllllll");
        response.data.forEach((element) => {
      
          this.setState((state) => {
            state.userslots.push(element.number);
            state.usercarrier.push(element.carrierid);
            state.userdates.push(element.dateofapp);
            state.userconfirmed.push(element.isselected);
          });
        });
        console.log(this.state.userslots+" --- "+this.state.usercarrier+"--"+this.state.userconfirmed)

        var s = '<div className="userapp"><table><tr><th>slot</th><th>carrier</th><th>date</th><th>is Confirmed</th></tr>';
        console.log("skata");
        var i=0;
        this.state.userslots.forEach((element) => {
          var confirmed = "";
          console.log(this.state.userconfirmed[i])
          if(this.state.userconfirmed[i] == true){
            confirmed="Confiremd";
          }else{
            confirmed="Not Confiremd";
          }
          s +='<tr><td>'+ element +'</td>';
          s +='<td>'+ this.state.usercarrier[i] +'</td>';
          s +='<td>'+this.state.userdates[i]+'</td>';
          s +='<td>'+confirmed+'</td>';
          s +='</tr>'
          i++;
        });
        s += '<tr></tr></table></div>';
           var view =(
            <div dangerouslySetInnerHTML={{ __html: s }} />
          );
          ReactDOM.render(view, document.getElementById("show"));
      }
      
    }).catch(error => {
        console.log(error);
      });
    }
  

   submitappointment(i) {
    const apdata={"number":i,
      "isselected":false,
      "isreserved":true,
      "carrierid":this.state.selectedId,
      "dateofapp":this.state.datetosend,
      "userid":localStorage.getItem("userid")}

     

      console.log(apdata +"to insert to appointment");

      axios({
        url: "/storeappointmentstoredis",
        method: "post",
        mode: "no-cors",
        headers: {
          common: {
            Accept: "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Access-Control-Allow-Origin": "*",
          },
          "Access-Control-Allow-Origin": "*",
        },
        proxy: {
          host: "localhost",
          port: "5002",
        },
        data: apdata,
      })
        .then((response) => {
          console.log(response.statusText);
          console.log("data inserted to appointment--------------");
        })
        .catch(function (error) {
          console.log("data inserted to appointment--------------");
          console.log(error);
        });
  }

  // calendarchange(event) {
  //   this.setState({
  //     [event.target.name]: event.target.value,
  //   });
  //   console.log(this.state.date);
  // }
  calendarchange = (date) => this.setState({ date });

  componentDidMount() {
    this.getCarriers();
  }

  including(y, i) {
    var including = y.includes(i);
    if (including == true) {
      return "not-available";
    } else {
      return "available";
    }
    // return including;
  }
  including2(y, i) {
    var including = y.includes(i);
    if (including == true) {
      return "Μη Διαθέσμιμο";
    } else {
      return "Διαθέσμιμο";
    }
    // return including;
  }


  handleCalendarSubmit(e) {
    //this.setState(this.baseState);
    const { date } = this.state;
    const dateformated = Moment(date).format("YYYY-MM-DD");
    var carid = this.state.selectedId;
    this.setState({ datetosend: dateformated });
    console.log(dateformated);
    console.log(this.state.selectedId);
    e.preventDefault();

    var formBody = new FormData();
    formBody.append("dateofapp", dateformated);
    console.log(formBody);

    axios({
      url: "/appointments_carrier_perday/" + carid,
      method: "post",
      mode: "no-cors",
      headers: {
        common: {
          Accept: "application/json",
          "Content-Type": "application/x-www-form-urlencoded",
          "Access-Control-Allow-Origin": "*",
        },
        "Access-Control-Allow-Origin": "*",
      },
      proxy: {
        host: "localhost",
        port: "5002",
      },
      data: formBody,
    })
      .then((response) => {
        console.log(response.statusText);
        if (response.status < 200 || response.status >= 300) {
          //throw new Error(response.statusText);
          console.log(response);
        } else {
          this.setState({slots:[]});
          console.log("okokkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk"+response.data.length);
          if(response.data.length != 0){
          console.log(response.data);
          console.log(response.data[0].number);
         
          console.log(this.state.slots+" must be nulllllllllllllllllllllll");
          response.data.forEach((element) => {
            const number = element.number;
            const isSelected = element.isselected;
            this.setState((state) => {
              state.slots.push(number);
            });
          });
        
          console.log(this.state.slots+" new slotssssssssssssssss");
  

          console.log(this.including(this.state.slots, 2));
          const tableElement = (
            <div className="appoin-table">
              <table>
                <tr>
                  <th>Ώρα</th>
                  <th>Διαθεσιμότητα</th>
                  <th>Επιλογή</th>
                </tr>
                <tr>
                  <td>10:00-11:00</td>
                  <td className={this.including(this.state.slots, 1)}>
                    {this.including2(this.state.slots, 1)}
                  </td>
                  <td>
                    <button type="submit" onClick={()=>{this.submitappointment(1)}}>Search</button>
                  </td>
                </tr>
                <tr>
                  <td>11:00-12:00</td>
                  <td className={this.including(this.state.slots, 2)}>
                    {this.including2(this.state.slots, 2)}
                  </td>
                  <td>
                    <button type="submit" onClick={()=>{this.submitappointment(2)}}>Search</button>
                  </td>
                </tr>
                <tr>
                  <td>12:00-13:00</td>
                  <td className={this.including(this.state.slots, 3)}>
                    {this.including2(this.state.slots, 3)}
                  </td>
                  <td>
                    <button type="submit" onClick={()=>{this.submitappointment(3)}}>Search</button>
                  </td>
                </tr>
                <tr>
                  <td>13:00-14:00</td>
                  <td className={this.including(this.state.slots, 4)}>
                    {this.including2(this.state.slots, 4)}
                  </td>
                  <td>
                    <button type="submit" onClick={()=>{this.submitappointment(4)}}>Search</button>
                  </td>
                </tr>
                <tr>
                  <td>14:00-15:00</td>
                  <td className={this.including(this.state.slots, 5)}>
                    {this.including2(this.state.slots, 5)}
                  </td>
                  <td>
                    <button type="submit" onClick={()=>{this.submitappointment(5)}}>Search</button>
                  </td>
                </tr>
                <tr>
                  <td>15:00-16:00</td>
                  <td className={this.including(this.state.slots, 6)}>
                    {this.including2(this.state.slots, 6)}
                  </td>
                  <td>
                    <button type="submit" onClick={()=>{this.submitappointment(6)}}>Search</button>
                  </td>
                </tr>
              </table>
            </div>
          );
          ReactDOM.render(tableElement, document.getElementById("table"));
          }else{

            const tableElement = (
              <div className="appoin-table">
                <table>
                  <tr>
                    <th>Ώρα</th>
                    <th>Διαθεσιμότητα</th>
                    <th>Επιλογή</th>
                  </tr>
                  <tr>
                    <td>10:00-11:00</td>
                    <td className={this.including(this.state.slots, 1)}>
                      {this.including2(this.state.slots, 1)}
                    </td>
                    <td>
                      <button type="submit" onClick={()=>{this.submitappointment(1)}}>Search</button>
                    </td>
                  </tr>
                  <tr>
                    <td>11:00-12:00</td>
                    <td className={this.including(this.state.slots, 2)}>
                      {this.including2(this.state.slots, 2)}
                    </td>
                    <td>
                      <button type="submit" onClick={()=>{this.submitappointment(2)}}>Search</button>
                    </td>
                  </tr>
                  <tr>
                    <td>12:00-13:00</td>
                    <td className={this.including(this.state.slots, 3)}>
                      {this.including2(this.state.slots, 3)}
                    </td>
                    <td>
                      <button type="submit" onClick={()=>{this.submitappointment(3)}}>Search</button>
                    </td>
                  </tr>
                  <tr>
                    <td>13:00-14:00</td>
                    <td className={this.including(this.state.slots, 4)}>
                      {this.including2(this.state.slots, 4)}
                    </td>
                    <td>
                      <button type="submit" onClick={()=>{this.submitappointment(4)}}>Search</button>
                    </td>
                  </tr>
                  <tr>
                    <td>14:00-15:00</td>
                    <td className={this.including(this.state.slots, 5)}>
                      {this.including2(this.state.slots, 5)}
                    </td>
                    <td>
                      <button type="submit" onClick={()=>{this.submitappointment(5)}}>Search</button>
                    </td>
                  </tr>
                  <tr>
                    <td>15:00-16:00</td>
                    <td className={this.including(this.state.slots, 6)}>
                      {this.including2(this.state.slots, 6)}
                    </td>
                    <td>
                      <button type="submit" onClick={()=>{this.submitappointment(6)}}>Search</button>
                    </td>
                  </tr>
                </table>
              </div>
            );
            ReactDOM.render(tableElement, document.getElementById("table"));

          }
          return response;
        }
      })
      .catch(function (error) {
        console.log("hello ERROR");
        console.log(error);
      });
  }

  async getCarriers() {
    let data = await axios
      .get("http://0.0.0.0:8001/carriers")
      .then(function (response) {
        return response;
      })
      .catch(function (error) {
        console.log(error);
      });

    console.log("mutsas maracas");
    console.log(data);
    const dt = data.data.data;
    //const last = dt.slice()
    dt.slice(0, 10).forEach((element) => {
      const obj = Object.values(element);

      this.setState((state) => {
        const options = state.options.push({ label: obj[1], value: obj[0] });
      });
      // this.state.options.push(options=[{"value":obj[0],"name":obj[1]}]);
    });
    console.log(this.state.options);
    this.setState({ loading: false });
  }

  change = (selectedOption) => {
    const gap = (
      <div ></div>)
      ReactDOM.render(gap, document.getElementById("table"));
      this.setState({ datetosend: new Date() });
    console.log(selectedOption.label, selectedOption.value);
    this.setState({
      selectedItem: selectedOption.label,
      selectedId: selectedOption.value,
    });
    console.log(this.state.selectedItem);
    const calendarelement = (
      <div class="control">
        <Calendar
          name="date"
          value={this.state.date}
          onChange={this.calendarchange}
        />

        <button onClick={this.handleCalendarSubmit}>Search</button>
      </div>
    );
    ReactDOM.render(calendarelement, document.getElementById("cale"));
    console.log(this.state.date);
  };

  render() {
    // this.getCarriers();
    if (this.state.loading) return <Loader />;
    return (
      <div className="main">
        <div className="main-body">
        <h3 id="header">Arrange your appointment</h3>
          <div className="myappoint">
          <button onClick={this.showapp}>Show my appointments</button>
          <div id="show"></div>
          </div>
          <div className="container">
            <div className="flex-child-left">
              <Select
                className="drop"
                name="selectedItem"
                value={this.state.selectedItem}
                options={this.state.options}
                onChange={this.change.bind(this)}
              >
                {this.state.selectedItem}
              </Select>
            </div>
            <div id="carrier" className="flex-child-right">
              <label className="lbl">{this.state.selectedItem}</label>
            </div>
          </div>
          <div id="cale" className="container-down"></div>
          <div id="table" className="container-table"></div>
        </div>
      </div>
    );
  }
}
