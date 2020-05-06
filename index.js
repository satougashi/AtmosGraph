var express = require('express')
var sqlite3 = require('sqlite3')
var app = express()
const dbName = 'atmos.db'


app.use(express.static('files'))

app.get('/data', function (req, res) {
  var db = new sqlite3.Database(dbName)

  var table = req.query.table
  var sql = "SELECT * FROM " + table

  var where = []
  var data = []
  if (req.query.start_at) {
    data.push(Date.parse(req.query.start_at))
    where.push('datetime(create_at, \'localtime\') > ?')
  }

  if (req.query.end_at) {
    data.push(Date.parse(req.query.end_at))
    // data.push(req.query.end_at)
    // where.push('datetime(create_at, \'localtime\') < datetime(?, \'localtime\')')
    where.push('datetime(create_at, \'localtime\') < ?')
  }

  if (where.length) {
    sql += ' WHERE ' + where.join(' AND ');
  }
  console.log(sql);
  console.log(data);
  db.all(sql, data, function (err, rows) {
    res.send(JSON.stringify(rows));
  });

  db.close();
});

var server = app.listen(80, function () {
  var host = server.address().address;
  var port = server.address().port;

  console.log('Example app listening at http://%s:%s', host, port);
});