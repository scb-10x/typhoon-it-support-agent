# Test Suite Documentation

Comprehensive test coverage for the Typhoon IT Support ticketing system.

## Test Files

### `test_ticket_tools.py`
**Purpose**: Unit tests for ticket tool functions  
**Coverage**: Real user scenarios, edge cases, integration tests, and performance tests

#### Test Categories

**Real User Scenarios** (`TestRealUserScenarios`)
- `test_user_reports_urgent_printer_issue`: Urgent ticket creation with SLA tracking
- `test_complete_ticket_lifecycle`: Full workflow from creation to resolution
- `test_escalation_workflow`: Priority escalation and SLA recalculation
- `test_bulk_ticket_management`: Managing multiple related tickets
- `test_sla_breach_scenario`: SLA breach detection and tracking
- `test_search_and_filter_tickets`: Finding related tickets

**Edge Cases** (`TestEdgeCases`)
- `test_create_ticket_with_invalid_priority`: Invalid input handling
- `test_update_nonexistent_ticket`: Non-existent resource handling
- `test_get_nonexistent_ticket`: Error responses for missing data
- `test_assign_ticket_invalid_agent`: Invalid agent assignment
- `test_add_duplicate_tags`: Duplicate tag prevention
- `test_set_invalid_category`: Invalid category validation
- `test_update_invalid_status`: Status validation
- `test_empty_ticket_list`: Empty result handling
- `test_search_with_no_results`: No matches handling
- `test_concurrent_updates_simulation`: Concurrent update handling
- `test_ticket_with_empty_description`: Minimal data handling
- `test_very_long_ticket_content`: Large content handling
- `test_special_characters_in_ticket`: Unicode and special characters
- `test_multiple_status_changes`: State transition tracking
- `test_sla_targets_for_all_priorities`: SLA calculation verification
- `test_ticket_history_tracks_all_changes`: Complete audit trail

**Integration Tests** (`TestIntegration`)
- `test_full_support_workflow_with_escalation`: Complete support workflow
- `test_multi_ticket_incident_management`: Incident with multiple tickets

**Performance Tests** (`TestPerformance`)
- `test_many_tickets_search_performance`: Search with 100+ tickets
- `test_ticket_with_many_comments`: Handling 50+ comments

### `test_ticket_api.py`
**Purpose**: API endpoint tests  
**Coverage**: Real user scenarios, edge cases, and integration tests via HTTP

#### Test Categories

**Real User API Scenarios** (`TestRealUserAPIScenarios`)
- `test_user_creates_ticket_via_api`: Ticket creation endpoint
- `test_admin_views_all_tickets`: List all tickets
- `test_filter_tickets_by_status`: Status filtering
- `test_get_ticket_details`: Single ticket retrieval
- `test_update_ticket_status_workflow`: Status update workflow
- `test_assign_ticket_to_agent`: Agent assignment
- `test_add_tags_to_ticket`: Tag management
- `test_set_ticket_category`: Category assignment
- `test_advanced_search`: Multi-criteria search
- `test_bulk_update_tickets`: Bulk operations
- `test_export_tickets_csv`: CSV export
- `test_get_ticket_statistics`: Dashboard statistics
- `test_get_available_agents`: Agent list retrieval

**Edge Cases API** (`TestEdgeCasesAPI`)
- `test_create_ticket_missing_required_fields`: Validation
- `test_get_nonexistent_ticket`: 404 handling
- `test_update_nonexistent_ticket`: Update validation
- `test_delete_nonexistent_ticket`: Delete validation
- `test_assign_invalid_agent`: Invalid agent handling
- `test_set_invalid_status`: Status validation
- `test_set_invalid_priority`: Priority validation
- `test_set_invalid_category`: Category validation
- `test_bulk_update_empty_list`: Empty bulk operations
- `test_bulk_update_partial_failure`: Partial failure handling
- `test_search_with_no_results`: Empty search results
- `test_filter_invalid_status`: Invalid filter parameters
- `test_very_long_subject`: Large data handling
- `test_unicode_and_special_characters`: Unicode support
- `test_concurrent_updates_same_ticket`: Concurrent API calls

**Integration API Tests** (`TestIntegrationAPI`)
- `test_full_ticket_lifecycle_via_api`: Complete API workflow
- `test_multi_ticket_incident_via_api`: Multi-ticket incident management

### `test_tools.py`
**Purpose**: Basic tool function tests  
**Coverage**: Utility tools and document search

#### Test Categories
- Time formatting tests
- Document search functionality
- Case-insensitive search
- Special character handling

### `test_api.py`
**Purpose**: Core API endpoint tests  
**Coverage**: Health checks, chat endpoints, session management

### Other Test Files
- `test_config.py`: Configuration management
- `test_models.py`: Data model validation
- `test_prompts.py`: Prompt template tests
- `test_workflow.py`: Workflow execution tests
- `test_router_node.py`: Routing logic tests

## Running Tests

### Run All Tests
```bash
cd agentic-workflow
pytest tests/
```

### Run Specific Test File
```bash
pytest tests/test_ticket_tools.py
pytest tests/test_ticket_api.py
```

### Run Specific Test Class
```bash
pytest tests/test_ticket_tools.py::TestRealUserScenarios
pytest tests/test_ticket_api.py::TestEdgeCasesAPI
```

### Run Specific Test
```bash
pytest tests/test_ticket_tools.py::TestRealUserScenarios::test_complete_ticket_lifecycle
```

### Run with Coverage
```bash
pytest tests/ --cov=src.typhoon_it_support --cov-report=html
```

### Run with Verbose Output
```bash
pytest tests/ -v
```

### Run Only Failed Tests
```bash
pytest tests/ --lf
```

## Test Coverage Summary

### Ticket Tools Coverage
- ✅ **Create operations**: Normal, urgent, bulk creation
- ✅ **Read operations**: Get by ID, search, filter, list
- ✅ **Update operations**: Status, priority, assignment, tags, category
- ✅ **Delete operations**: Single ticket deletion
- ✅ **SLA tracking**: All priority levels, breach detection
- ✅ **History tracking**: Complete audit trail
- ✅ **Assignment system**: Valid/invalid agents
- ✅ **Tag management**: Add, duplicate prevention
- ✅ **Category system**: Valid/invalid categories
- ✅ **Bulk operations**: Multiple ticket updates
- ✅ **Search**: Text search, filtering, no results
- ✅ **Edge cases**: Invalid inputs, missing data, concurrency

### API Endpoints Coverage
- ✅ `GET /tickets`: List with filters
- ✅ `GET /tickets/{id}`: Single ticket retrieval
- ✅ `POST /tickets`: Create ticket
- ✅ `PATCH /tickets/{id}`: Update ticket
- ✅ `DELETE /tickets/{id}`: Delete ticket
- ✅ `POST /tickets/{id}/assign`: Assign to agent
- ✅ `POST /tickets/{id}/tags`: Add tags
- ✅ `POST /tickets/{id}/category`: Set category
- ✅ `GET /tickets/search/advanced`: Advanced search
- ✅ `POST /tickets/bulk/update`: Bulk updates
- ✅ `GET /tickets/export/csv`: CSV export
- ✅ `GET /tickets/stats/summary`: Statistics
- ✅ `GET /tickets/agents`: Agent list

## Test Data

Tests use in-memory storage (`_mock_tickets`) that resets before each test via `reset_tickets` fixture.

### Default Test Data
- Ticket counter starts at 1000
- Available agents: 4 agents with different specializations
- SLA targets: Priority-based (urgent: 15min/4hrs, high: 1hr/8hrs, normal: 4hrs/24hrs, low: 8hrs/48hrs)

### Sample Tickets Created
Tests create tickets with varied:
- Priorities: low, normal, high, urgent
- Statuses: new, open, pending, solved, closed
- Categories: hardware, software, network, email, vpn, etc.
- Languages: English and Thai text
- Content: Short, long, with special characters

## Best Practices

1. **Isolation**: Each test is independent with clean state
2. **Realistic**: Tests simulate actual user workflows
3. **Comprehensive**: Cover happy paths and edge cases
4. **Documented**: Clear test names and docstrings
5. **Fast**: Use in-memory storage, no external dependencies
6. **Maintainable**: Organized into logical test classes

## CI/CD Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    cd agentic-workflow
    pytest tests/ --cov --cov-report=xml
```

## Adding New Tests

When adding features, ensure:
1. Add unit tests in `test_ticket_tools.py`
2. Add API tests in `test_ticket_api.py`
3. Test both success and failure cases
4. Include edge cases and validation
5. Update this documentation
