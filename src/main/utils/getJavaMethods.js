function parseJavaClass() {

	const allTables = document.querySelectorAll('table[class="overviewSummary"]');
	
	const javaClass = {
		fields: [],
		constructors: [],
		methods: []
	}
	
	allTables.forEach(table => {
		let summary = table.getAttribute("Summary");
	
		if (summary.includes("Field")) {
			javaClass.fields = parseTable(table.children[1], 'field');
		} else if (summary.includes("Constructor")) {
			javaClass.constructors = parseTable(table.children[1], 'constructor');
		} else if (summary.includes("Method")) {
			javaClass.methods = parseTable(table.children[1], 'methods');
		} else {
			console.warn('Unrecognized table: ' + summary)
		}
	});
	return javaClass;
}

function parseTable(tableRows, type) {
	const tableContents = []
	for (let i = 1; i < tableRows.childElementCount; i++) {
			let row = tableRows.children[i];
			// console.log("DEBUG: row #" + i + ": " + row.innerText);
			switch(type){
				case 'field':
				// if (row.childElementCount > 1) {
				// 	tableContents.push({
				// 		"modifiers": row.children[0].innerText.split(' ')[0],
				// 		"fieldName": row.children[0].innerText.split(' ')[-1]
				// 	})
				// } else {
				// 	// inherited field
				// }
					break;
				case 'constructor':
					tableContents.push(row.innerText.split('\n')[0]);
					break;
				case 'methods':
					tableContents.push({
						returnType: row.children[0].innerText,
						nameAndParams: row.children[1].innerText.split('\n')[0]
					});
					break;
				default:
					console.warn('Unrecognized type table: ', type)
			}
			
	}
	// console.log("DEBUG: table parsed: " + JSON.stringify(tableContents));
	return tableContents
}

console.log(JSON.stringify(parseJavaClass()))