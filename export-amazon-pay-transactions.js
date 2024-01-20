var transactionNodes = document.querySelectorAll('#transaction-desktop div.a-fixed-left-grid-inner div.a-col-right');
arrTransactions = [];
transactionNodes.forEach((node) => {
	let amount = node.querySelector('div.a-row div.a-text-right span').innerText;
	let description = node.querySelector('div.a-row div.a-text-left div.pad-header-text span').innerText;
	let transDate = node.querySelector('div.a-row div.a-text-left > span.a-color-tertiary').innerText;

	if (description.indexOf('On-hold for') == -1 && description.indexOf('Released from')) {
	arrTransactions.push({
		trans_date: transDate,
		trans_amount: amount,
		trans_desc: description
	});
	}
});
console.log(arrTransactions);
