import pytest
from app import schemas


def test_get_all_posts_unauthenticated(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200

    def validate(post):
        return schemas.PostOut(**post)

    posts_list = list(map(validate, res.json()))
    assert len(posts_list) == len(test_posts)


def test_get_one_post_unauthenticated(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/8000000")
    assert res.status_code == 404


@pytest.mark.parametrize("title, content, is_published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, is_published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "is_published": is_published})
    assert res.status_code == 201
    created_post = res.json()
    assert created_post['title'] == title
    assert created_post['content'] == content
    assert created_post['is_published'] == is_published
    assert created_post['owner_id'] == test_user['id']


def test_create_post_missing_is_published(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "arbitrary title", "content": "arbitrary content"})
    assert res.status_code == 422


def test_create_post_unauthenticated(client, test_posts):
    res = client.post("/posts/", json={"title": "arbitrary title", "content": "arbitrary content", "is_published": True})
    assert res.status_code == 401


def test_unauthenticated_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/8000000")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {"title": "updated title", "content": "updated content", "is_published": True}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 200
    updated_post = res.json()
    assert updated_post['title'] == data['title']
    assert updated_post['content'] == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {"title": "updated title", "content": "updated content", "is_published": True}
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthenticated_user_update_post(client, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}", json={"title": "x", "content": "y", "is_published": True})
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {"title": "updated title", "content": "updated content", "is_published": True}
    res = authorized_client.put("/posts/8000000", json=data)
    assert res.status_code == 404


@pytest.mark.parametrize("search", ["first", "2nd", ""])
def test_get_posts_with_search(authorized_client, test_posts, search):
    res = authorized_client.get(f"/posts/?search={search}")
    assert res.status_code == 200
