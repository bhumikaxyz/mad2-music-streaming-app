const Navbar = Vue.component('Navbar', {
    template: `<nav class="navbar fixed-top navbar-expand-lg bg-primary-subtle">
    <div class="container-fluid">
      <router-link to ="/" class="navbar-brand mb-0 mx-5 h1 display-6 fw-bold">
        <img
          src="static/images/musical-note.png"
          alt="Logo"
          width="30"
          height="30"
          class="d-inline-block align-text-top me-2"
        />
        cuhu
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div
        class="collapse navbar-collapse navbar-nav me-auto mb-2 mb-lg-0 d-flex justify-content-between align-items-center"
        id="navbarSupportedContent"
      >
        <div class="ms-auto d-flex mx-5">

          <router-link class="nav-link active" to="/home">Home</router-link>

          <router-link class="nav-link active" to="">Dashboard</router-link>

          <router-link class="nav-link active" to=""
            >Your Playlists</router-link
          >

          <router-link class="nav-link active" to="">Profile</router-link>

          <router-link class="nav-link active" to="">Logout</router-link>
        </div>
      </div>
    </div>
  </nav>`
})


export default Navbar;