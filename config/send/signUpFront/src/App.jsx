import React, { Component} from 'react';


class App extends Component {
    constructor(){
        super()
        this.state = {
            firstName: '',
            lastName: '',
            email: '',
            phone: '',
            Labor: '',
            userName: '',
            password: ''
        }
    }

    changeFirstName(event){
        this.setState({
            firstName: event.target.value
        })
    }

    changeLastName(event){
        this.setState({
            lastName: event.target.value
        })
    }

    changeemail(event){
        this.setState({
            email: event.target.value
        })
    }

    changePhone(event){
        this.setState({
            phone: event.target.value
        })
    }

    changelabor(event){
        this.setState({
            Labor: event.target.value
        })
    }

    changeUserName(event){
        this.setState({
            userName: event.target.value
        })
    }

    changeUserName(event){
        this.setState({
            userName: event.target.value
        })
    }

    changepassword(event){
        this.setState({
            password: event.target.value
        })
    }
    
    render() {
        return (
            <div className = 'container'>
                <div className = 'form-div'>
                    <form>
                        <table>
                            <tbody>

                                <tr>
                                    <td> First Name </td>
                                </tr>
                                <tr>
                                    <td>
                                    <input type = "text" id = "firstName" placeholder="Gary" onChange = {this.changeFirstName} value = {this.state.firstName} required></input>
                                    </td>
                                </tr>

                                <tr>
                                    <td> Last Name </td>
                                </tr>
                                <tr>
                                    <td>
                                    <input type = "text" id = "lastName" placeholder="Brown" onChange = {this.changeLasttName} value = {this.state.lastName} required></input>
                                    </td>
                                </tr>

                                <tr>
                                    <td> Email </td>
                                </tr>
                                <tr>
                                    <td> <input type = "text" id = "email" placeholder="johndoe@email.com" onChange = {this.changeemail} value = {this.state.email} required></input></td>
                                </tr>
                                
                                <tr>
                                    <td> Phone Number </td>
                                </tr>
                                <tr>
                                    <td> <input type = "text" id = "phonenumber" placeholder="x-xxx-xxx-xxxx" onChange = {this.changePhone} value = {this.state.phone} pattern = "[0-9]{1}-[0-9]{3}-[0-9]{3}-[0-9]{4}" required></input></td>
                                </tr>

                                <tr>
                                    <td>Labor (Keywords)</td>
                                </tr>
                                <tr>
                                    <td> <input type = "text" id = "keywords" placeholder="Ex. painter, landscaper, renovator..."  onChange = {this.changeLabor} value = {this.state.Labor} required></input></td>
                                </tr>

                                <tr>
                                    <td> Username </td>
                                </tr>
                            
                                <tr>
                                    <td> <input type = "text" id = "username" placeholder="Username" onChange = {this.changeUserName} value = {this.state.userName} required></input></td>
                                </tr>
                            
                                <tr>
                                    <td> Password </td>
                                </tr>
                                <tr>
                                    <td> <input type = "text" id = "password" placeholder="Password" maxlength="30" onChange = {this.changepassword} value = {this.state.password} required></input></td>
                                </tr>
                                
                            
                                <tr>
                                    <td>
                                        <input type = "submit" className = "create_profile" value = "Create Account"></input>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </form>
                </div>

            </div>
        );
    }
}

export default App;