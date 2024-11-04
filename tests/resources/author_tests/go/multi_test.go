
package main

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestFindGitSlug(t *testing.T) {
	t.Run("Test CodeCommit HTTP URL", func(t *testing.T) {
		provider, slug, err := findGitSlug("https://git-codecommit.us-east-2.amazonaws.com/v1/repos/my-repo", "")
		assert.NoError(t, err)
		assert.Equal(t, "CodeCommit", provider)
		assert.Equal(t, "my-repo", slug)
	})

	t.Run("Test CodeCommit SSH URL", func(t *testing.T) {
		provider, slug, err := findGitSlug("ssh://git-codecommit.us-east-2.amazonaws.com/v1/repos/my-repo", "")
		assert.NoError(t, err)
		assert.Equal(t, "CodeCommit", provider)
		assert.Equal(t, "my-repo", slug)
	})

	t.Run("Test GitHub HTTP URL", func(t *testing.T) {
		provider, slug, err := findGitSlug("https://github.com/user/repo.git", "")
		assert.NoError(t, err)
		assert.Equal(t, "GitHub", provider)
		assert.Equal(t, "github.com/user/repo", slug)
	})

	t.Run("Test GitHub SSH URL", func(t *testing.T) {
		provider, slug, err := findGitSlug("git@github.com:user/repo.git", "")
		assert.NoError(t, err)
		assert.Equal(t, "GitHub", provider)
		assert.Equal(t, "github.com/user/repo", slug)
	})

	t.Run("Test GitHub Enterprise HTTP URL", func(t *testing.T) {
		provider, slug, err := findGitSlug("https://ghe.example.com/user/repo.git", "ghe.example.com")
		assert.NoError(t, err)
		assert.Equal(t, "GitHubEnterprise", provider)
		assert.Equal(t, "ghe.example.com/user/repo", slug)
	})

	t.Run("Test GitHub Enterprise SSH URL", func(t *testing.T) {
		provider, slug, err := findGitSlug("git@ghe.example.com:user/repo.git", "ghe.example.com")
		assert.NoError(t, err)
		assert.Equal(t, "GitHubEnterprise", provider)
		assert.Equal(t, "ghe.example.com/user/repo", slug)
	})

	t.Run("Test Unknown URL", func(t *testing.T) {
		provider, slug, err := findGitSlug("https://example.com/user/repo.git", "")
		assert.NoError(t, err)
		assert.Equal(t, "", provider)
		assert.Equal(t, "https://example.com/user/repo.git", slug)
	})
}