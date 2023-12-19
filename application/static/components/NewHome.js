export default {
    template: `<div>
    <div class="container py-5 my-4">
        <h2>All Tracks</h2>
          <div class="container d-flex justify-content-between align-items-center mb-3">
    
          <form method="get" action="" class="d-flex">
            <div class="form-group mb-0 me-2">
              <select id="filter_type" name="filter_type">
                <option value="title">Title</option>
                <option value="artist">Artist</option>
                <option value="rating">Rating</option>
              </select>
            </div>
            <div class="form-group mb-0 me-2">
              <input type="text" id="filter_value" name="filter_value">
            </div>
            <div class="form-group mb-0 me-2">
              <div><button type="submit" class="btn btn-outline-primary btn-sm">Submit</button></div>
            </div>
          </form>
        
        <!-- ------------------------------------------------------------------------------------ -->

        <!-- Add Song button for creator -->
          <h2 class="text-end">
            <button class="btn btn-success btn-sm" @click='buttonAddSong'>+ Add Song</button>
          </h2>  
        </div>

        <!-- ----------------------------------------------------------------------------------------- -->


        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-5 g-3 mb-3">
            <div v-for="song in songs.songs" :key="song.id" class="col">
                <div class="card shadow-sm bg-danger-subtle mb-3">
                <img src="static/images/song.png" class="img-thumbnail rounded mb-0 shadow-sm mx-auto" alt="song" width="200 px" height="200 px"/>
                <div class="card-body px-2">
                <p class="card-text">
                <p class="mb-0">{{ song.title }}</p>
                <p><small>{{ song.artist }}</small></p>
                </p>
                <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group margin-right-2">
                        <button type="button" class="btn btn-sm btn-outline-secondary" @click='buttonPlaySong(song.id)'>Play</button>
                        <button type="button" class="btn btn-sm btn-outline-secondary" @click='buttonEditSong(song.id)'>Edit</button>
                        <button type="button" class="btn btn-sm btn-outline-secondary"@click='buttonDeleteSong(song.id)'>Delete</button>
                     </div>
                    <small class="text-body-secondary">{{ song.duration }}</small>
                </div>
                </div>
            </div>    
        </div>  
        </div>    

        <hr class="mt-3">
        <h2 class="mb-3">All Albums</h2>
        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-5 g-3 mb-3">
            <div v-for="album in albums.albums" :key="album.id" class="col">
                <div class="card shadow-sm bg-danger-subtle mb-3">
                <img src="static/images/album.png" class="img-thumbnail rounded mb-0 shadow-sm mx-auto" alt="song" width="200 px" height="200 px"/>
                <div class="card-body padding-top-0">
                <p class="card-text">
                <p class="mb-0">{{ album.name }}</p>
                <p><small>{{ album.artist}}</small></p>
                </p>
                <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                        <button type="button" class="btn btn-sm btn-outline-secondary">View</button>
                        <button type="button" class="btn btn-sm btn-outline-secondary">Edit</button>
                        <button type="button" class="btn btn-sm btn-outline-secondary">Delete</button>
                     </div>
                </div>
                </div>
            </div>    
        </div>  
        </div>  
       
    </div>
    </div>`,

    data() {
        return {
            songs: [],
            albums: []
        }   
    },
    mounted() {
        this.getSongs();
        this.getAlbums()
    },
    methods: {
        async getSongs() {
            try {
              const response = await fetch('http://127.0.0.1:5000/api/songs');
              if (response.ok) {
                this.songs = await response.json();
              } else {
                const errorData = await response.json();
                console.error('Error fetching songs:', errorData);
              }
            } catch (error) {
              console.error('Error fetching songs:', error);
            }
          },
      
          async getAlbums() {
            try {
              const response = await fetch('http://127.0.0.1:5000/api/albums');
              if (response.ok) {
                this.albums = await response.json();
              } else {
                const errorData = await response.json();
                console.error('Error fetching albums:', errorData);
              }
            } catch (error) {
              console.error('Error fetching albums:', error);
            }
          },

        buttonAddSong(){
            this.$router.push({ path: '/upload-song' })
        },

        buttonPlaySong(song_id){
            this.$router.push({ name: "Play Song", params: {id: song_id}})
        },

        buttonEditSong(song_id){
            console.log(song_id)
            this.$router.push({ name: "Update Song", params: {id: song_id}})
        },

        async buttonDeleteSong(song_id){
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/song/${song_id}`, {
                  method: 'DELETE',
                  headers: {
                    'Content-Type': 'application/json'
                  },
                });
        
                if (response.ok) {
                  console.log('Song deleted successfully');
                  this.songs = this.songs.filter(song => song.id !== song_id);
                } else {
                  const errorData = await response.json();
                  console.error('Error deleting song:', errorData);
                }
              } catch (error) {
                console.error('Error deleting song:', error);
              }
          },    
    },   
}