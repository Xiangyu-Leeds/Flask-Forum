function member_del(obj, id) {
    layer.confirm('Are you sure you want to delete it permanently? (Non-recoverable)', function (index) {
        //Send asynchronously delete data
        //We'll use async later, but we'll use async here
        $.get("/delete?id=" + id);

        layer.msg('have deleted', {icon: 1, time: 1000});
        setTimeout("location.reload()", "500")
    });
}


function cancel(obj, id) {
    layer.confirm('Are you sure you want to cancel', function (index) {
        //Send asynchronously delete data
        //We'll use async later, but we'll use async here
        $.get("/cancel?id=" + id);

        layer.msg('have canceled!', {icon: 1, time: 1000});
        setTimeout("location.reload()", "500")
    });
}

// function change(obj, id1,id2,id3) {
//     $.get("/qa/like/?answer_id= user_id= question_id= " + id1,+id2,+id3);
//     setTimeout("location.reload()", "50")
//
//
// }

function change1(obj, id) {
    $.get("/uncompleted_issue?id=" + id);
    setTimeout("location.reload()", "50")

}

function important(obj, id) {
    layer.confirm('Are you sure you want to put it in the important？', function (index) {
        //Send asynchronously delete data
        //We'll use async later, but we'll use async here
        $.get("/favour?id=" + id);

        layer.msg('important!', {icon: 1, time: 1000});
        setTimeout("location.reload()", "500")
    });
}


layui.use(['layer', 'form'], function () {
    var layer = layui.layer;
});

function add_space(obj) {
    layer.open({
        type: 2,
        area: ['50%', '50%'],
        content: '/qa/add_space',
        title: "Add a space",
        end: function () {
            location.reload()
        }
    });
}

layui.use(['layer', 'form'], function () {
    var layer = layui.layer;
});

function add_avatar(obj) {
    layer.open({
        type: 2,
        area: ['80%', '80%'],
        content: '/qa/add_avatar',
        title: "Add an avatar",
        end: function () {
            location.reload()
        }
    });
}

layui.use(['layer', 'form'], function () {
    var layer = layui.layer;
});

function profile(obj,id) {
    layer.open({
        type: 2,
        area: ['80%', '80%'],
        content: '/qa/check_information?id=' + id,
        title: "Check personal information",
        end: function () {
            location.reload()
        }
    });
}

// layui.use(['layer', 'form'], function () {
//     var layer = layui.layer;
// });
// function check_follow(obj,id) {
//     layer.open({
//         type: 2,
//         area: ['80%', '80%'],
//         content: '/qa/check_follow',
//         title: "Check personal follow",
//         end: function () {
//             location.reload()
//         }
//     });
// }
layui.use(['layer', 'form'], function () {
    var layer = layui.layer;
});
function change_password(obj,id) {
    layer.open({
        type: 2,
        area: ['60%', '60%'],
        content: '/auth/change_password',
        title: "Check personal follow",
        end: function () {
            location.reload()
        }
    });
}
