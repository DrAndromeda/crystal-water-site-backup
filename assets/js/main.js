/* ============================================
   Crystal Water — JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  // Header scroll effect
  const header = document.getElementById('header');
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 50);
  });

  // Burger menu
  const burger = document.getElementById('burger');
  const nav = document.getElementById('nav');
  burger.addEventListener('click', () => {
    nav.classList.toggle('active');
    burger.classList.toggle('active');
  });
  nav.querySelectorAll('.nav__link').forEach(link => {
    link.addEventListener('click', () => nav.classList.remove('active'));
  });

  // Bottles counter
  const bottlesInput = document.getElementById('bottles');
  const decrementBtn = document.getElementById('decrement');
  const incrementBtn = document.getElementById('increment');
  const totalEl = document.getElementById('orderTotal');
  const PRICE = 100;

  function updateTotal() {
    const qty = parseInt(bottlesInput.value) || 1;
    totalEl.innerHTML = `<span>Разом:</span><span class="form__total-price">${qty * PRICE} ₴</span>`;
  }

  decrementBtn.addEventListener('click', () => {
    let val = parseInt(bottlesInput.value) || 1;
    if (val > 1) bottlesInput.value = val - 1;
    updateTotal();
  });
  incrementBtn.addEventListener('click', () => {
    let val = parseInt(bottlesInput.value) || 1;
    if (val < 20) bottlesInput.value = val + 1;
    updateTotal();
  });
  bottlesInput.addEventListener('change', () => {
    let val = parseInt(bottlesInput.value) || 1;
    if (val < 1) val = 1;
    if (val > 20) val = 20;
    bottlesInput.value = val;
    updateTotal();
  });

  // Phone formatting
  const phoneInput = document.getElementById('phone');
  phoneInput.addEventListener('input', (e) => {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length === 0) { e.target.value = ''; return; }
    if (value.startsWith('38')) value = value.substring(2);
    let formatted = '+38';
    if (value.length > 0) formatted += ' (' + value.substring(0, 3);
    if (value.length >= 4) formatted += ') ' + value.substring(3, 6);
    if (value.length >= 7) formatted += '-' + value.substring(6, 8);
    if (value.length >= 9) formatted += '-' + value.substring(8, 10);
    e.target.value = formatted;
  });

  // Form submission
  const form = document.getElementById('orderForm');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const city = document.getElementById('city').value;
    const address = document.getElementById('address').value.trim();
    const bottles = document.getElementById('bottles').value;
    const comment = document.getElementById('comment').value.trim();

    if (!name || !phone || !city || !address) {
      alert('Будь ласка, заповніть всі обов\'язкові поля');
      return;
    }

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = 'Відправляємо...';

    const message = encodeURIComponent(
      `🆕 Нове замовлення!\n\n` +
      `👤 Ім'я: ${name}\n` +
      `📞 Телефон: ${phone}\n` +
      `📍 Адреса: ${city}, ${address}\n` +
      `💧 Бутилів: ${bottles}\n` +
      `💵 Сума: ${parseInt(bottles) * PRICE} ₴\n` +
      (comment ? `💬 Коментар: ${comment}` : '')
    );

    try {
      // Send to Telegram bot
      const response = await fetch(
        `https://api.telegram.org/bot${window.BOT_TOKEN || ''}/sendMessage`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            chat_id: '237228075',
            text: `🆕 Нове замовлення!\n\n👤 Ім'я: ${name}\n📞 Телефон: ${phone}\n📍 Місто: ${city}\n🏠 Адреса: ${address}\n💧 Бутилів: ${bottles}\n💰 Сума: ${parseInt(bottles) * PRICE} грн${comment ? '\n💬 Коментар: ' + comment : ''}`
          })
        }
      );

      if (response.ok) {
        form.reset();
        updateTotal();
        alert('✅ Дякуємо! Ваше замовлення прийнято. Ми зв\'яжемося з вами найближчим часом.');
      } else {
        // Fallback: open Telegram
        window.open(`https://t.me/CrystalWaterBro_bot?start=order_${encodeURIComponent(name)}_${phone}`, '_blank');
        alert('✅ Дякуємо! Ваше замовлення передано через Telegram.');
      }
    } catch (err) {
      window.open(`https://t.me/CrystalWaterBro_bot?start=order_${encodeURIComponent(name)}_${phone}`, '_blank');
      alert('✅ Дякуємо! Ваше замовлення передано через Telegram.');
    }

    submitBtn.disabled = false;
    submitBtn.innerHTML = originalText;
  });

});
