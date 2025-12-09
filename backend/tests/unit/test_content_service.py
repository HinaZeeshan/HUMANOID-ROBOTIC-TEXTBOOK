"""
Unit tests for the Content service in the Humanoid Robotics Textbook project.
"""
import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from backend.src.services.content_service import ContentService
from backend.src.models.book_content import Module, Chapter, ContentBlock


class TestContentService:
    """Unit tests for the ContentService class."""

    @pytest.fixture
    def mock_db_session(self):
        """Mock database session for testing."""
        return Mock(spec=Session)

    @pytest.fixture
    def content_service(self, mock_db_session):
        """Create a ContentService instance for testing."""
        return ContentService(mock_db_session)

    def test_create_module(self, content_service):
        """Test module creation."""
        title = "Test Module"
        slug = "test-module"
        description = "A test module"

        # Mock the database operations
        with patch_db_operations(content_service.db):
            module = content_service.create_module(
                title=title,
                slug=slug,
                description=description,
                order=1
            )

            # Verify the module was created with correct attributes
            assert module.title == title
            assert module.slug == slug
            assert module.description == description
            assert module.order == 1
            # Verify database operations were called
            content_service.db.add.assert_called_once()
            content_service.db.commit.assert_called_once()

    def test_get_module(self, content_service):
        """Test module retrieval."""
        module_id = "test-module-id"

        # Create a mock module
        mock_module = Module(
            id=module_id,
            title="Test Module",
            slug="test-module",
            description="A test module",
            order=1
        )

        # Mock the query result
        mock_query = Mock()
        mock_query.filter_by.return_value.first.return_value = mock_module
        content_service.db.query.return_value = mock_query

        result = content_service.get_module(module_id)
        assert result.id == module_id
        content_service.db.query.assert_called_once_with(Module)
        mock_query.filter_by.assert_called_once_with(id=module_id)

    def test_get_module_by_slug(self, content_service):
        """Test module retrieval by slug."""
        module_slug = "test-module"

        # Create a mock module
        mock_module = Module(
            id="test-module-id",
            title="Test Module",
            slug=module_slug,
            description="A test module",
            order=1
        )

        # Mock the query result
        mock_query = Mock()
        mock_query.filter_by.return_value.first.return_value = mock_module
        content_service.db.query.return_value = mock_query

        result = content_service.get_module_by_slug(module_slug)
        assert result.slug == module_slug
        content_service.db.query.assert_called_once_with(Module)
        mock_query.filter_by.assert_called_once_with(slug=module_slug)

    def test_create_chapter(self, content_service):
        """Test chapter creation."""
        module_id = "test-module-id"
        title = "Test Chapter"
        slug = "test-chapter"
        content = "Chapter content"

        # Mock the database operations
        with patch_db_operations(content_service.db):
            chapter = content_service.create_chapter(
                module_id=module_id,
                title=title,
                slug=slug,
                content=content
            )

            # Verify the chapter was created with correct attributes
            assert chapter.module_id == module_id
            assert chapter.title == title
            assert chapter.slug == slug
            assert chapter.content == content
            # Verify database operations were called
            content_service.db.add.assert_called_once()
            content_service.db.commit.assert_called_once()

    def test_get_chapter(self, content_service):
        """Test chapter retrieval."""
        chapter_id = "test-chapter-id"

        # Create a mock chapter
        mock_chapter = Chapter(
            id=chapter_id,
            module_id="test-module-id",
            title="Test Chapter",
            slug="test-chapter",
            content="Chapter content",
            order=1
        )

        # Mock the query result
        mock_query = Mock()
        mock_query.filter_by.return_value.first.return_value = mock_chapter
        content_service.db.query.return_value = mock_query

        result = content_service.get_chapter(chapter_id)
        assert result.id == chapter_id
        content_service.db.query.assert_called_once_with(Chapter)
        mock_query.filter_by.assert_called_once_with(id=chapter_id)

    def test_list_chapters_by_module(self, content_service):
        """Test listing chapters by module."""
        module_id = "test-module-id"

        # Create mock chapters
        mock_chapters = [
            Chapter(
                id="chapter1",
                module_id=module_id,
                title="Chapter 1",
                slug="chapter-1",
                content="Content 1",
                order=1
            ),
            Chapter(
                id="chapter2",
                module_id=module_id,
                title="Chapter 2",
                slug="chapter-2",
                content="Content 2",
                order=2
            )
        ]

        # Mock the query result
        mock_query = Mock()
        mock_query.filter.return_value.order_by.return_value.all.return_value = mock_chapters
        content_service.db.query.return_value = mock_query

        result = content_service.list_chapters_by_module(module_id)
        assert len(result) == 2
        assert result[0].id == "chapter1"
        assert result[1].id == "chapter2"
        content_service.db.query.assert_called_once_with(Chapter)
        mock_query.filter.assert_called_once()
        mock_query.filter.return_value.order_by.assert_called_once()

    def test_create_content_block(self, content_service):
        """Test content block creation."""
        chapter_id = "test-chapter-id"
        content_type = "text"
        content = "This is test content."
        title = "Test Block"

        # Mock the database operations
        with patch_db_operations(content_service.db):
            block = content_service.create_content_block(
                chapter_id=chapter_id,
                type=content_type,
                content=content,
                title=title,
                order=1
            )

            # Verify the block was created with correct attributes
            assert block.chapter_id == chapter_id
            assert block.type == content_type
            assert block.content == content
            assert block.title == title
            assert block.order == 1
            # Verify database operations were called
            content_service.db.add.assert_called_once()
            content_service.db.commit.assert_called_once()

    def test_list_content_blocks_by_chapter(self, content_service):
        """Test listing content blocks by chapter."""
        chapter_id = "test-chapter-id"

        # Create mock blocks
        mock_blocks = [
            ContentBlock(
                id="block1",
                chapter_id=chapter_id,
                type="text",
                content="Content block 1",
                title="Block 1",
                order=1
            ),
            ContentBlock(
                id="block2",
                chapter_id=chapter_id,
                type="code",
                content="print('hello')",
                title="Code Block",
                order=2
            )
        ]

        # Mock the query result
        mock_query = Mock()
        mock_query.filter.return_value.order_by.return_value.all.return_value = mock_blocks
        content_service.db.query.return_value = mock_query

        result = content_service.list_content_blocks_by_chapter(chapter_id)
        assert len(result) == 2
        assert result[0].id == "block1"
        assert result[1].type == "code"
        content_service.db.query.assert_called_once_with(ContentBlock)
        mock_query.filter.assert_called_once()
        mock_query.filter.return_value.order_by.assert_called_once()


class TestModuleModel:
    """Unit tests for the Module model."""

    def test_module_creation(self):
        """Test Module model creation."""
        module = Module(
            title="Test Module",
            slug="test-module",
            description="A test module",
            order=1,
            learning_objectives=["Objective 1", "Objective 2"],
            prerequisites=["Prereq 1"]
        )

        assert module.title == "Test Module"
        assert module.slug == "test-module"
        assert module.description == "A test module"
        assert module.order == 1
        assert module.learning_objectives == ["Objective 1", "Objective 2"]
        assert module.prerequisites == ["Prereq 1"]

    def test_module_defaults(self):
        """Test Module model default values."""
        module = Module(
            title="Test Module",
            slug="test-module"
        )

        assert module.title == "Test Module"
        assert module.slug == "test-module"
        assert module.description == ""
        assert module.order == 0
        assert module.learning_objectives == []
        assert module.prerequisites == []


class TestChapterModel:
    """Unit tests for the Chapter model."""

    def test_chapter_creation(self):
        """Test Chapter model creation."""
        chapter = Chapter(
            module_id="test-module-id",
            title="Test Chapter",
            slug="test-chapter",
            content="Chapter content"
        )

        assert chapter.module_id == "test-module-id"
        assert chapter.title == "Test Chapter"
        assert chapter.slug == "test-chapter"
        assert chapter.content == "Chapter content"

    def test_chapter_defaults(self):
        """Test Chapter model default values."""
        chapter = Chapter(
            module_id="test-module-id",
            title="Test Chapter",
            slug="test-chapter"
        )

        assert chapter.module_id == "test-module-id"
        assert chapter.title == "Test Chapter"
        assert chapter.slug == "test-chapter"
        assert chapter.content == ""
        assert chapter.order == 0


class TestContentBlockModel:
    """Unit tests for the ContentBlock model."""

    def test_content_block_creation(self):
        """Test ContentBlock model creation."""
        block = ContentBlock(
            chapter_id="test-chapter-id",
            type="text",
            content="Block content",
            title="Test Block"
        )

        assert block.chapter_id == "test-chapter-id"
        assert block.type == "text"
        assert block.content == "Block content"
        assert block.title == "Test Block"

    def test_content_block_defaults(self):
        """Test ContentBlock model default values."""
        block = ContentBlock(
            chapter_id="test-chapter-id",
            type="code",
            content="print('hello')"
        )

        assert block.chapter_id == "test-chapter-id"
        assert block.type == "code"
        assert block.content == "print('hello')"
        assert block.title == ""
        assert block.order == 0


# Helper function to patch database operations
def patch_db_operations(mock_db):
    """Helper to patch common database operations."""
    mock_db.add = Mock()
    mock_db.commit = Mock()
    mock_db.refresh = Mock()
    return mock_db