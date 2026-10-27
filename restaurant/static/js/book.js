// Little Lemon booking form - uses the fetch API to talk to /bookings
const FIRST_SLOT = 10, LAST_SLOT = 20; // 10 AM - 8 PM

const dateEl = document.getElementById('reservation_date');
const slotEl = document.getElementById('reservation_slot');
const nameEl = document.getElementById('first_name');
const formEl = document.getElementById('booking-form');
const listEl = document.getElementById('bookings');
const headingEl = document.getElementById('bookings-heading');
const msgEl = document.getElementById('message');
const btnEl = document.getElementById('reserve-btn');

function slotLabel(h) {
  const suffix = h >= 12 ? 'PM' : 'AM';
  const hour = h > 12 ? h - 12 : h;
  return `${hour} ${suffix}`;
}

// Local date as YYYY-MM-DD (avoids the UTC shift of toISOString)
function todayString() {
  const d = new Date();
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${mm}-${dd}`;
}

function showMessage(text, isError) {
  msgEl.textContent = text;
  msgEl.className = isError ? 'error' : 'success';
}

// Fetch bookings for the selected date, then redraw list + slot dropdown
async function loadBookings() {
  const date = dateEl.value;
  if (!date) return;
  try {
    const res = await fetch(`/bookings?date=${encodeURIComponent(date)}`);
    const data = await res.json();
    const booked = data.map(b => b.fields);

    headingEl.textContent = `Bookings For ${date}`;
    listEl.innerHTML = '';
    if (booked.length === 0) {
      listEl.innerHTML = '<p class="no-booking">No Booking</p>';
    } else {
      booked.forEach(b => {
        const p = document.createElement('p');
        p.textContent = `${b.first_name} - ${slotLabel(b.reservation_slot)}`;
        listEl.appendChild(p);
      });
    }
    buildSlots(booked.map(b => b.reservation_slot));
  } catch (err) {
    showMessage('Could not load bookings. Please try again.', true);
  }
}

// Booked slots are disabled (greyed out) so duplicates cannot be chosen
function buildSlots(bookedSlots) {
  slotEl.innerHTML = '';
  let firstFree = null;
  for (let h = FIRST_SLOT; h <= LAST_SLOT; h++) {
    const opt = document.createElement('option');
    opt.value = h;
    opt.textContent = slotLabel(h);
    if (bookedSlots.includes(h)) {
      opt.disabled = true;
      opt.textContent += ' (booked)';
    } else if (firstFree === null) {
      firstFree = h;
    }
    slotEl.appendChild(opt);
  }
  const allBooked = firstFree === null;
  slotEl.disabled = allBooked;
  btnEl.disabled = allBooked;
  if (!allBooked) slotEl.value = firstFree;
}

formEl.addEventListener('submit', async (e) => {
  e.preventDefault();
  msgEl.textContent = '';
  const payload = {
    first_name: nameEl.value.trim(),
    reservation_date: dateEl.value,
    reservation_slot: Number(slotEl.value),
  };
  try {
    const res = await fetch('/bookings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (res.ok) {
      showMessage('Your reservation is confirmed!', false);
      nameEl.value = '';
    } else {
      showMessage(data.error || 'Booking failed.', true);
    }
  } catch (err) {
    showMessage('Network error. Please try again.', true);
  }
  loadBookings();
});

// Changing the date refreshes the booking data
dateEl.addEventListener('change', () => { msgEl.textContent = ''; loadBookings(); });

// Current date is selected automatically when the page opens
dateEl.value = todayString();
loadBookings();
