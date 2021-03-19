

BASE_URL = '/api/cupcakes'
$list = $("#cupcake-list")
$img = $('#cupcake-img')
$desc = $('#cupcake-description')
//sends axios request to server api for cupcakes
async function getCupcakes(){
    res = await axios.get(BASE_URL).then(function(result){
        console.log(result.data.cupcakes)
        let cupcakes = result.data.cupcakes
        return cupcakes
        
    })
    return res
}

//adds all cupcakes to the dom
function populateCupcakes(cupcakes){
    for(let cake of cupcakes){
        addCupcake(cake)
    }
}

    //adds a single cupcake element to the dom with a delete button
function addCupcake(cake){
    $li = $('<li>')
    $del = $('<button>')
    $del.text('X')
    $del.addClass('float-right btn btn-danger btn-sm delete')

    $li.addClass('list-group-item')
    $li.data('toggle','popover')
    $li.data('img',cake.image)
    $li.data('id',cake.id)
    $li.text(`${cake.size} ${cake.flavor} cupcake - rated a ${cake.rating}`)
    
    $li.appendTo($list).append($del)
}

//gets and adds all cupcakes - a composite function
async function loadCakes(){
    cakes = await getCupcakes()
    populateCupcakes(cakes)
}

loadCakes()
// imgUpdate.call()

//handels form submission
$('#cupcake-form').on('submit',function(e){
    e.preventDefault()
    $inputs = $("#cupcake-form :input")
    let cupcake={}
    for(let input of $inputs){
        if(input.tagName == 'BUTTON'){
            continue
        }
        
        cupcake[input.name]=input.value
    }
    sendCake(cupcake)
    this.reset()
})

//adds cake to swl database through server
async function sendCake(cake){

    await axios.post(BASE_URL,cake).then(function(response){
        addCupcake(response.data.cupcake)
        $('#cupcake-form')[0].reset()
    })
}
//deletes cupcake from database and dom 
async function deleteCupcake(){
    parent = $(this).parent()
    id = parent.data('id')
    await axios.delete(`${BASE_URL}/${id}`).then(function(response){
        parent.remove()
    }).catch(function(error){
        console.log(error)
    })
}
$list.on('click','.delete',deleteCupcake)



$list.on('click','.list-group-item', imgUpdate)
function imgUpdate(){
    console.log(this)
    img = $(this).data('img')
    desc = $(this).text()
    $img.attr('src',img)
    $desc.text(desc.slice(0,-1))
}

  $(window).bind("load", function () {
    imgUpdate.call($('li')[0]) 
  });