const mongoose = require('mongoose');

const signUpTemplate = new mongoose.Schema({


    firstName:{
        type: String,
        
    },

    lastName:{
        type: String,
        
    },

    email:{
        type: String,
        
    },

    phone:{
        type: String,
        
    },

    Labor:{
        type: String,
        

    },

    userName:{
            type: String,
            

    },

    password: {
            type: String,
            
    },
  

    date:{
        type: Date,
        default: Date.now
    }

});


module.exports = mongoose.model('userRegistration', signUpTemplate );