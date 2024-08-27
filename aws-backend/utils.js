// utility functions that are used in multiple api routes
// neede dto rename to utils to avoid conflict with built in util function 

const AWS = require('aws-sdk');
AWS.config.update({
    region: 'eu-north-1'
})

// const dynamodb = new AWS.DynamoDB.DocumentClient();

    function buildResponse(statusCode, body) {
        return {
        statusCode: statusCode,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
        }
    }

    module.exports = {
        buildResponse
    };
