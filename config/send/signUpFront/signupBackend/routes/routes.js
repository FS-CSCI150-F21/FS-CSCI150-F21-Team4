const { response } = require('express');
const express = require('express');
const router = express.Router();
const signUp = require('../models/signUpModels');


router.post('/signup', (request, response)=> {
    const signUpUser = new signUp({
        firstName: request.body.firstName,
        lastName: request.body.lastName,
        email: request.body.email,
        phone: request.body.phone,
        labor: request.body.Labor,
        userName: request.body.userName,
        password: request.body.password
        
      
    });

     signUpUser.save()
        .then(data =>{
            response.json(data);
        })
        .catch(error =>{
            response.json(error);

        })

});



module.exports = router;
