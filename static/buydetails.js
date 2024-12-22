let urlParams = new URLSearchParams(window.location.search);
		let itemName = urlParams.get('item');

		let borrowButton = document.getElementById('borrow-btn');
		borrowButton.addEventListener('click', () => {
			let name = document.getElementById('name').value;
			let email = document.getElementById('email').value;
			let phone = document.getElementById('phone').value;

			alert(`Thank you, ${name}! You have successfully borrowed ${itemName}. We will contact you soon at ${phone} or ${email}.`);
		});