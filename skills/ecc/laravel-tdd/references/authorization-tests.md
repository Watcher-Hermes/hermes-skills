## Authorization Tests

```php
public function test_users_can_update_own_posts(): void
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $this->actingAs($user)
        ->put(route('posts.update', $post), ['title' => 'Updated'])
        ->assertRedirect();
}

public function test_users_cannot_update_others_posts(): void
{
    $post = Post::factory()->create();
    $this->actingAs(User::factory()->create())
        ->put(route('posts.update', $post), ['title' => 'Hacked'])
        ->assertForbidden();
}

public function test_gate_before_grants_super_admin_full_access(): void
{
    $super = User::factory()->create(['role' => 'super-admin']);
    $post = Post::factory()->create();

    $this->actingAs($super)
        ->delete(route('posts.destroy', $post))
        ->assertRedirect();

    $this->assertSoftDeleted($post);
}
```