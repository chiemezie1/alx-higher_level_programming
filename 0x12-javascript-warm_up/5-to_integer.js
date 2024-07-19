#!/usr/bin/node
const num = Number.isInteger(process.argv[2], 10);
if (!isNaN(num)) {
  console.log('My number: ' + num);
} else {
  console.log('Not a number');
}
