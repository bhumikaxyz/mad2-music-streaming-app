export default {
    template: `
    <div>
    <div class="container py-4">
        <h2>All Tracks</h2>
          <div class="container d-flex justify-content-between align-items-center mb-3">
    
          <form method="get" action="" class="d-flex">
            <div class="form-group mb-0 me-2">
              <label for="filter_type">Filter Type</label>
              <select id="filter_type" name="filter_type">
                <option value="title">Title</option>
                <option value="artist">Artist</option>
                <option value="rating">Rating</option>
              </select>
            </div>
            <div class="form-group mb-0 me-2">
              <label for="filter_value">Filter Value</label>
              <input type="text" id="filter_value" name="filter_value">
            </div>
            <div class="form-group mb-0 me-2">
              <div><button type="submit" class="btn btn-outline-primary btn-sm">Submit</button></div>
            </div>
          </form>
        
        <!-- ------------------------------------------------------------------------------------ -->
    
    
        <!-- Add Song button for creator -->
          <h2 class="text-end">
            <button class="btn btn-success btn-sm">+ Add Song</button>
          </h2>  
        </div>
        <!-- ----------------------------------------------------------------------------------------- -->
         
    
        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-5 g-3 mb-3">
          <!-- {% for song in songs %} -->
          <div class="col">
            <div class="card shadow-sm bg-danger-subtle mb-3">
              <img src="" class="img-thumbnail rounded mb-0 shadow-sm mx-auto" alt="song" width="200 px" height="200 px";>
              <div class="card-body padding-top-0">
                <p class="card-text">
                  <p class="mb-0">{{ song.title }}</p>
                  <p><small>{{ song.artist }}</small></p>
                </p>
                <div class="d-flex justify-content-between align-items-center">
                  <div class="btn-group">
                    <button type="button" class="btn btn-sm btn-outline-secondary" href="">
                      Play
                    </button>
                    <!-- {% if current_user.is_creator and song.creator_id == current_user.id %} -->
                      <button type="button" class="btn btn-sm btn-outline-secondary" href="">
                        Edit
                      </button>
                      <button type="button" class="btn btn-sm btn-outline-secondary" href="">
                        Delete
                      </button>
                    <!-- {% endif %} -->
                  </div>
                  <small class="text-body-secondary">{{ song.duration }}</small>
                </div>
              </div>
            </div>
          </div>
          <!-- {% endfor %} -->
        </div>
      
        <hr class="mt-3 ">
        <h2 class="mb-3">All Albums</h2>
        <!-- {% if albums %} -->
        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-5 g-3">
          <!-- {% for album in albums %} -->
          <div class="col">
            <div class="card shadow-sm bg-danger-subtle">
              <img src="" class="img-thumbnail rounded mb-1 shadow-sm mx-auto" alt="song" width="200 px" height="200 px";>
              <div class="card-body padding-top-0">
                <p class="card-text">
                  <p class="mb-0">{{ album.name }}</p>
                  <p><small>{{ album.artist }}</small></p>
                </p>
                <div class="d-flex justify-content-between align-items-center">
                  <div class="btn-group btn-sm">
                    <button type="button" class="btn btn-sm btn-outline-secondary" href="">
                      View
                    </button>
                    <!-- {% if current_user.is_creator and album.creator_id == current_user.id %} -->
                      <button type="button" class="btn btn-sm btn-outline-secondary" >
                        Edit
                      </button>
                      <button type="button" class="btn btn-sm btn-outline-secondary" >
                        Delete
                      </button>
                    <!-- {% endif %} -->
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- {% endfor %} -->
        </div>
    </div>  
    </div>
    `
}