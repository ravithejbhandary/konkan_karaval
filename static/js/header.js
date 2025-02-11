class MyHeader extends HTMLElement {
    connectedCallback() {
        this.innerHTML = 
        `
        
<!-- Navbar -->
<header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container">
            <!-- Logo -->
            <a class="navbar-brand" href="#">
                <img src="/static/images/2 2.png" alt="Karaval Konkanis Australia Logo" width="120">
            </a>

            <!-- Mobile Toggle Button (Fixed) -->
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <!-- Navbar Links -->
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="#home">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="#about">About Us</a></li>
                    <li class="nav-item"><a class="nav-link" href="#news">News</a></li>

                    <!-- Fixed Dropdown Menu -->
<li class="nav-item dropdown">
    <div class="dropdown">
        <button class="dropbtn">Events</button>
        <div class="dropdown-content">
            <a href="Past_Events.html">Past Events</a>
            <a href="upevents.html">Upcoming Events</a>
        </div>
    </div>
</li>


                    <li class="nav-item"><a class="nav-link" href="#gallery">Gallery</a></li>
                    <li class="nav-item"><a class="nav-link" href="#contact">Contact Us</a></li>

                    <!-- Join Button (Custom Button Kept as It Is) -->
                    <li class="nav-item">
                        <button class="join-button">Join our Family</button>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</header>

<!-- Popup -->
<div id="popup" class="popup-container">
    <div class="popup-content">
        <p id="poppy">Are you already a part of the family?</p>
        <button onclick="alreadyMember()">Yes</button>
        <button onclick="notMember()">No</button>
        <button class="close-btn" onclick="closePopup()">Close</button>
    </div>
</div>

</body>
</html>







    `
    }
}
customElements.define('my-header', MyHeader)