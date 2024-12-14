/*Here’s a shorter summary of the JavaScript code and its functionality:

### **Overview**
This code is for a web app that handles user and meeting management. It uses AJAX to interact with a backend API for creating, updating, and deleting meetings and users, while offering a calendar interface to manage and view meetings.

### **Key Features**
1. **User Authentication**: 
   - If `authToken` or `user` is missing in `localStorage`, the user is redirected to login.
   - Admins can manage users and meetings, while regular users have limited functionality.

2. **AJAX Requests**:
   - Fetch meetings (`GET /api/meeting/`), users (`GET /api/user`), and handle CRUD operations for meetings and users (POST, PUT, DELETE).

3. **Role-Based UI**:
   - Admin functionalities (e.g., adding/deleting users, adding meetings) are hidden from regular users.

4. **Calendar**:
   - Displays a dynamic calendar where users can see meetings scheduled for each day.
   - Meetings can be added, updated, and deleted using modals.

5. **Event Handlers**:
   - Includes handlers for events like navigating between months, opening modals, and confirming deletions.

### **Important Functions**
- **`renderCalendar()`**: Renders the calendar with meetings for each day.
- **`openModal()`**: Opens a modal to add a new meeting for a selected date.
- **`deleteMeetingConfirmation()`**: Displays a confirmation modal before deleting a meeting.
- **`filterUserNames()`**: Filters and displays users based on input.
- **`openDisplayModalForDate()`**: Displays all meetings for a selected day.

### **User Management**
- Admins can update user info and delete users via modals.
- Regular users can only update their own details.

### **Meeting Management**
- Users and admins can add, view, or delete meetings. Meetings are associated with specific users and displayed on the calendar.

### **UI Interactions**
- **Modals**: Used for adding, viewing, and deleting meetings and users.
- **Navigation**: Users can navigate between months on the calendar.

### **Enhancements**
1. **Error Handling**: Currently, errors are logged to the console. You could improve this with user-friendly error messages.
2. **Form Validation**: Add checks for required fields and password confirmation.
3. **UI Improvements**: Consider adding loading indicators and better form feedback.

In short, this script provides a user- and meeting-management system with a calendar interface, CRUD operations, and role-based access control. */

let user = localStorage.getItem('user');
let token = localStorage.getItem('authToken');

let events = [];
let users = [];


$(document).ready(function(){
   
        if(!user || !token){
            window.location.href = '/';
        } else {    
            
            // hiding admin functionalities from user
            if(JSON.parse(user).role === 'user'){
                $('#v-pills-addmeetings-tab').hide()
                $('#v-pills-addmeetings').hide()
                $('#v-pills-usermanagment-tab').hide()
                $('#v-pills-usermanagment').hide()
                $('#th-action-display-model').hide()
            }

            // fetching all meetings' data from backend
            $.ajax({
                type: 'GET',
                url: '/api/meeting/',
                headers: {'Authorization': `Bearer ${token}`},
                success: function(data){
                    events = data.meetings;
                    renderCalendar(currMonth, currYear, events); 
                }      
            });

            // fetching all users for dropdown
            $.ajax({
                type: 'GET',
                url: '/api/user',
                headers: {'Authorization': `Bearer ${token}`},
                success: function(response){
                    users = response.users;
                }
            });  
 
        }

        // logout Functionality :
        $('#logout-tab').on('click', function(){
            localStorage.removeItem('authToken');
            localStorage.removeItem('user');
        });

        // Add Meetings Functionality :
        $('#addmeeting-btn').on('click', function(e){
            e.preventDefault();
            var un = $('#search_user_id').val();
            var time = $('#time').val();
            var pf = $('#platform').val();
            var msg = $('#msg').val();
            var url = $('#url').val();
            var date = $('#modal-date').text();
            const data = {username:un,platform:pf,time:time,date:date,url:url,msg:msg};

            $.ajax({
                type: 'POST',
                url: '/api/meeting/',
                data: JSON.stringify(data),
                contentType: 'application/json',
                headers: {'Authorization': 'Bearer ' + token},
                success: function(data) {
                    generateCalendar(currentMonth, currentYear);
                    closeModal();
                    window.location.reload()
                    },
                error: function(xhr, status, error) {
                    console.log(xhr.responseText);
                    }
            })
            // console.log(data)
        });

        // Update user Details Finctionality :
        $('#updated_btn').on('click', function(e){
            e.preventDefault();
            
            var username = $('#updated_name').val();
            var email = $('#updated_email').val();
            var password = $('#updated_password').val();
            var confirmPassowrd = $('#updated_con_password').val();
            var user_id = $('#updated_user_id').val();

            if(password == confirmPassowrd){
                const data = {username:username, email:email, password:password};

                $.ajax({
                    type: 'PUT',
                    url: '/api/user/'+ user_id,
                    data: JSON.stringify(data),
                    contentType: 'application/json',
                    headers: {'Authorization': 'Bearer ' + token},
                    success: function(response) {
                        localStorage.setItem('user', JSON.stringify(response.user))
                        window.location.reload();
                        showSuccessToast('Changes saved succesfully')
                        },
                    error: function(xhr, status, error) {
                            console.log(xhr.responseText);
                        }
                })
                

            } else {
                console.log('Password and Confirm Password do not match');
            }
        });

        // Delete user Functionality :
        $('#confirmDelete').on('click', function(e){
            e.preventDefault()
            var id = $('#delete_user_id').val()
            console.log('deleted', id)

            $.ajax({
                type: 'DELETE',
                url: '/api/user/'+ id,
                headers: {'Authorization': 'Bearer ' + token},
                success: function(response) {
                    // console.log(response)
                    if(response.message == 'Success'){
                        localStorage.removeItem('authToken');
                        localStorage.removeItem('user');
                        window.location.reload();
                        
                    }
                },
                error: function(xhr, status, error) {
                    console.log(xhr.responseText);
                }

            })
        });
        
        // delete meeting :
        $('#confirmDeleteMeeting').on('click', function(e){
            var meetingId = $('#Confirm_meeting_id').val()
            console.log('meetingId', meetingId)
            
            $.ajax({
                type: 'DELETE',
                url: '/api/meeting/' + meetingId,
                headers: {'Authorization': 'Bearer ' + token},
                success: function(response) {
                    if(response.message === 'Success'){
                        showSuccessToast('Meeting Deleted Successfully');
                        window.location.reload()
                    }
                },
                error: function(xhr, status, error) {
                    console.log(xhr.responseText);
                }
            });
        });

        // USER MANAGEMENT FUNCTIONALITY :
        $('.user-managment-delete-btn').on('click', function(e) {
            e.preventDefault();
            var userId = $(this).data('delete-user-confirm-user-id');
            var username = $(this).data('delete-user-confirm-username');
            
            $('#delete-user-confirmation-message').text(`Are you sure you want to remove the"${username}'s" profile?`);
            $('#delete-user-confirmation-modal').removeClass('hidden');

            $('#confirmDeleteUser ').data('user-id', userId);
        });
    
        // Confirm deletion
        $('#confirmDeleteUser ').on('click', function() {
            var userId = $(this).data('user-id');
            // logic to delete the user using the userId

            $.ajax({
                type: 'DELETE',
                url: '/api/user/'+ userId,
                headers: {'Authorization': 'Bearer ' + token},
                success: function(response) {
                    if(response.message == 'Success'){
                        window.location.reload();
                        $('#delete-user-confirmation-modal').addClass('hidden');
                        showSuccessToast('User profile deleted successfully!')
                       
                    }
                },
                error: function(xhr, status, error) {
                    console.log(xhr.responseText);
                }

            })
        });
    
        // Close modal
        $('#closeDeleteUser ').on('click', function() {
            $('#delete-user-confirmation-modal').addClass('hidden');
        });
     
});


// Delete Meeting confirmation modal Functionality :
function deleteMeetingConfirmation(meetingId, userId) {
    
    const confirmationMessage = document.getElementById('confirmation-message');
    confirmationMessage.innerHTML = `Are you sure you want to delete the meeting ? 
                                    <input type='text' style='display:none' value=${meetingId} id='Confirm_meeting_id'>
                                    <input type='text' style='display:none' value=${userId} id='Confirm_meeting_userid'>
                                    `;
    
    const modal = document.getElementById('delete-meeting-confirmation-modal');
    modal.classList.remove('hidden'); 
};

document.getElementById('closeDeleteMeetingModal').addEventListener('click', function() {
    const modal = document.getElementById('delete-meeting-confirmation-modal');
    modal.classList.add('hidden'); // Hide the modal
});


// Filtering users and giving results :
function filterUserNames() {
    const input = document.getElementById('username').value.toLowerCase();
    const resultsDiv = document.getElementById('results');

    resultsDiv.innerHTML = '';

    const filteredUsers = users.filter(user => user.username.toLowerCase().includes(input));

    if (filteredUsers.length > 0) {
        filteredUsers.forEach(user => {
            const userItem = document.createElement('li');
            userItem.textContent = user.username;
            userItem.onclick = () => selectUser (user);
            resultsDiv.appendChild(userItem);
        });
        resultsDiv.classList.remove('hidden'); 
    } else {
        resultsDiv.classList.add('hidden'); 
    }
};

// select only registered user and selected user while assigning a meeting
function selectUser (user) {
    document.getElementById('username').value = user.username; 
    document.getElementById('search_user_id').value = user.id; 
    document.getElementById('results').classList.add('hidden'); 
};

// DISPLAY CALENDER
let currMonth = new Date().getMonth();
let currYear = new Date().getFullYear();

function renderCalendar(month, year, events) {
    const calendarDays = document.getElementById('calendarDays');
    calendarDays.innerHTML = '';

    const firstDay = new Date(year, month).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Create empty cells for days before the first day of the month
    for (let i = 0; i < firstDay; i++) {
        const emptyCell = document.createElement('div');
        calendarDays.appendChild(emptyCell);
    }

    // Create cells for each day of the month
    for (let day = 1; day <= daysInMonth; day++) {
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const eventsForDate = events.filter(e => e.date === dateStr);
        const dayCell = document.createElement('div');
        dayCell.className = 'bg-white p-4 rounded shadow cursor-pointer';
        dayCell.innerHTML = `<p class="text-lg font-bold">${day}</p>`;

        // Display the number of meetings for the day
        if (eventsForDate.length > 0) {
            dayCell.innerHTML += `<p class="text-sm">${eventsForDate.length} meeting(s)</p>`;
            dayCell.onclick = () => openDisplayModalForDate(eventsForDate);
        }

        let parsedUser  = JSON.parse(user);

        // Check if the logged-in user has events on this date
        const userEventsForDate = eventsForDate.filter(e => e.user_id === parsedUser.id);
        if (userEventsForDate.length > 0) {
            dayCell.classList.add('highlight'); // Add highlight class
        }

        calendarDays.appendChild(dayCell);
    }

    // Update the displayed month and year
    document.getElementById('currentMonth').innerText = new Date(year, month).toLocaleString('default', { month: 'long', year: 'numeric' });
};

document.getElementById('prevMonth').onclick = () => {
    currMonth--;
    if (currMonth < 0) {
        currMonth = 11;
        currYear--;
    }
    renderCalendar(currMonth, currYear, events);
};

document .getElementById('nextMonth').onclick = () => {
    currMonth++;
    if (currMonth > 11) {
        currMonth = 0;
        currYear++;
    }
    renderCalendar(currMonth, currYear, events);
};

function openDisplayModalForDate(meetings) {
    const modalBody = document.getElementById('modal-meeting-body');
    modalBody.innerHTML = ''; 

    let userRole;
    const parsedUser  = JSON.parse(user); 
    
    meetings.forEach(meeting => {
        const row = document.createElement('tr');
        if (meeting.user_id === parsedUser.id) {
            row.classList.add('highlight-row');
        }
        row.innerHTML = `
            <td style='display:none'>${meeting.id}</td>
            <td style='display:none'>${meeting.user_id}</td>
            <td>${meeting.username}</td>
            <td>${meeting.time}</td>
            <td>${meeting.platform}</td>
            <td><a href="${meeting.url}" target="_blank" class="text-blue-500 hover:underline">${meeting.url}</a></td>
            <td>${meeting.msg || '<i>--No Message--</i>'}</td>
            ${parsedUser.role === 'user' ? '' : `
            <td id='td-action-display-model-delete-btn'>
                <button  class="delete-meeting-btn" data-id="${meeting.id}">
                    <i class="fas fa-trash"></i> <!-- Trash bin icon -->
                </button>
                `}
            </td>
        `;
        modalBody.appendChild(row);
    });

    document.getElementById('display-modal-date').innerText = meetings[0].date; 
    document.getElementById('display-modal').classList.remove('hidden'); 
    if (userRole !== 'user') {
        $('.delete-meeting-btn').on('click', function() {
            const meetingId = $(this).data('id'); 
            const userId = $(this).closest('tr').find('td:nth-child(2)').text(); 
            deleteMeetingConfirmation(meetingId, userId);
        });
    }
};

function closeDisplayModal() {
    document.getElementById('display-modal').classList.add('hidden');
}

// Add MEETING CALENDER 
const calendarDates = document.getElementById('calendar-dates');
const currentDate = new Date();
let currentMonth = currentDate.getMonth();
let currentYear = currentDate.getFullYear();

function generateCalendar(month, year) {
    calendarDates.innerHTML = '';
    const firstDay = new Date(year, month).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Previous month dates
    const prevMonthDays = new Date(year, month, 0).getDate();
    for (let i = firstDay - 1; i >= 0; i--) {
        const date = prevMonthDays - i;
        calendarDates.innerHTML += `<div class="text-center text-gray-400">${date}</div>`;
    }

    // Current month dates
    for (let i = 1; i <= daysInMonth; i++) {
        calendarDates.innerHTML += `
            <div class="text-center bg-white p-4 rounded shadow cursor-pointer" onclick="openModal(${i})">
                <div id="date">${i}</div>
                <div class="text-sm text-gray-600" id="name-${i}"></div>
                <div class="text-sm text-gray-600" id="time-${i}"></div>
            </div>
        `;
    }

    // Next month dates
    const nextMonthDays = 42 - (firstDay + daysInMonth);
    for (let i = 1; i <= nextMonthDays; i++) {
        calendarDates.innerHTML += `<div class="text-center text-gray-400">${i}</div>`;
    }

    document.getElementById('currMonth').innerText = new Date(year, month).toLocaleString('default', { month: 'long', year: 'numeric' });
};

let selectedDate;

function openModal(date) {
    selectedDate = date;
    const fullDate = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(selectedDate).padStart(2, '0')}`;
    document.getElementById('modal-date').innerText = fullDate; 
    document.getElementById('modal').classList.remove('hidden');
};

function closeModal() {
    document.getElementById('modal').classList.add('hidden');
};

function saveEvent() {
    const user_id = document.getElementById('search_user_id').value;
    const time = document.getElementById('time').value;
    const platform = document.getElementById('platform').value;
    const url = document.getElementById('url').value;
    const msg = document.getElementById('msg').value;
    closeModal();
};

function goToPreviousMonth() {
    currentMonth--;
    if (currentMonth < 0) {
        currentMonth = 11; // December
        currentYear--;
    }
    generateCalendar(currentMonth, currentYear);
};

function goToNextMonth() {
    currentMonth++;
    if (currentMonth > 11) {
        currentMonth = 0; // January
        currentYear++;
    }
    generateCalendar(currentMonth, currentYear);
};

generateCalendar(currentMonth, currentYear);


// SETTING'S MODAL
document.getElementById('deleteAccount').addEventListener('click', function() {
    document.getElementById('setting-modal').classList.remove('hidden');
});

document.getElementById('closeSettingModal').addEventListener('click', function() {
    document.getElementById('setting-modal').classList.add('hidden');
});

document.getElementById('confirmDelete').addEventListener('click', function() {
    document.getElementById('setting-modal').classList.add('hidden');
});
