#!/usr/bin/node
const arg = process.argv[2];
const num = Number.parseInt(arg, 10);

if (!isNaN(num) && num.toString() === arg) {
  console.log(`My number: ${num}`);
} else {
  console.log('Not a number');
}
